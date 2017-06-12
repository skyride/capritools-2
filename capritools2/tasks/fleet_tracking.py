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
    fleet = api.get("/fleets/$fleet/")
    if fleet == None:
        db_fleet.active = False
        return

    db_fleet.motd = fleet['motd']
    db_fleet.voice_enabled = fleet['is_voice_enabled']
    db_fleet.registered = fleet['is_registered']
    db_fleet.free_move = fleet['is_free_move']
    db_fleet.save()


    print "Updated fleet %s" % fleet_id
