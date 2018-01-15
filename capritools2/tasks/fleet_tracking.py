import requests
import json

from capritools.celery import app
from capritools2.models import *
from capritools2.esi import ESI


@app.task(name="fleet_live_update_spawner")
def fleet_live_update_spawner():
    for fleet in Fleet.objects.filter(active=True).all():
        fleet_live_update.delay(fleet.id)
        print "Fired update for fleet %s" % fleet.id


@app.task(name="fleet_live_update")
def fleet_live_update(fleet_id):
    db_fleet = Fleet.objects.get(id=fleet_id)
    api = ESI(db_fleet.token, db_fleet.id)
    api.cache_time = 0

    # Update Fleet info
    old_members = set(map(lambda x: x.character, db_fleet.members.all()))
    fleet = api.get("/v1/fleets/$fleet/")
    if fleet == None:
        db_fleet.active = False
        db_fleet.save()
        return

    db_fleet.motd = fleet['motd']
    db_fleet.voice_enabled = fleet['is_voice_enabled']
    db_fleet.registered = fleet['is_registered']
    db_fleet.free_move = fleet['is_free_move']
    db_fleet.save()

    # Update fleet structure
    wings = api.get("/v1/fleets/$fleet/wings/")
    db_fleet.wings.exclude(id__in=map(lambda x: x['id'], wings)).delete()
    for wing in wings:
        db_wing = Fleet_Wing.get_or_create(wing['id'], db_fleet, wing['name'])
        db_wing.name = wing['name']
        db_wing.save()

        # Squads
        db_wing.squads.exclude(id__in=map(lambda x: x['id'], wing['squads'])).delete()
        for squad in wing['squads']:
            db_squad = Fleet_Squad.get_or_create(squad['id'], db_fleet, db_wing, squad['name'])
            db_squad.wing = db_wing
            db_squad.name = squad['name']
            db_squad.save()

    # Update members
    members = api.get("/v1/fleets/$fleet/members/")
    affiliations = []
    new_members = set(map(lambda x: Character.get_or_create_async(x['character_id']), members))
    db_fleet.members.exclude(character__in=new_members).delete()
    for member in members:
        try:
            db_member = db_fleet.members.get(character_id=member['character_id'])
        except Exception:
            db_member = Fleet_Member(fleet=db_fleet, character=Character.get_or_create_async(id=member['character_id']))

        # Fleet Position
        if member['wing_id'] > 0:
            db_member.wing = Fleet_Wing.objects.get(id=member['wing_id'])
        else:
            db_member.wing = None
        if member['squad_id'] > 0:
            db_member.squad = Fleet_Squad.objects.get(id=member['squad_id'])
        else:
            db_member.squad = None
        db_member.boss = member['role_name'].endswith("(Boss)")
        db_member.role = member['role']
        db_member.role_name = member['role_name']

        # Character
        if db_member.corporation == None:
            affiliations.append(db_member.character_id)

        # Meta
        if db_member.system != None:
            if db_member.system_id != member['solar_system_id']:
                Fleet_Jump(
                    fleet=db_fleet,
                    character=db_member.character,
                    from_system=db_member.system,
                    to_system_id=member['solar_system_id']
                ).save()
        db_member.system_id = member['solar_system_id']

        if db_member.ship != None:
            if db_member.ship_id != member['ship_type_id']:
                Fleet_ShipChange(
                    fleet=db_fleet,
                    character=db_member.character,
                    from_ship=db_member.ship,
                    to_ship_id=member['ship_type_id']
                ).save()
        db_member.ship_id = member['ship_type_id']

        if db_member.takes_fleet_warp != None:
            if db_member.takes_fleet_warp != member['takes_fleet_warp']:
                if member['takes_fleet_warp']:
                    Fleet_MemberEvent(
                        fleet=db_fleet,
                        character=db_member.character,
                        event="accept_fleetwarp"
                    ).save()
                else:
                    Fleet_MemberEvent(
                        fleet=db_fleet,
                        character=db_member.character,
                        event="exempt_fleetwarp"
                    ).save()
            db_member.takes_fleet_warp = member['takes_fleet_warp']

        db_member.save()

    # Create join/leave fleet events
    for character in old_members - new_members:
        Fleet_MemberEvent(
            fleet=db_fleet,
            character=character,
            event="leave"
        ).save()

    for character in new_members - old_members:
        Fleet_MemberEvent(
            fleet=db_fleet,
            character=character,
            event="join"
        ).save()


    # Get the character affiliations async
    if len(affiliations) > 0:
        fleet_live_fetch_affiliations.delay(affiliations, fleet_id)

    print "Updated fleet %s" % fleet_id


@app.task(name="fleet_live_fetch_affiliations")
def fleet_live_fetch_affiliations(ids, fleet_id):
    api = ESI()
    affiliations = api.post("/v1/characters/affiliation/", data=json.dumps(ids))

    for affiliation in affiliations:
        db_member = Fleet_Member.objects.get(character_id=affiliation['character_id'], fleet_id=fleet_id)
        db_member.corporation = Corporation.get_or_create_async(affiliation['corporation_id'])
        if "alliance_id" in affiliation:
            db_member.alliance = Alliance.get_or_create_async(affiliation['alliance_id'])
        db_member.save()
