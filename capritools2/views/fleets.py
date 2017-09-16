import re
import json

from django.shortcuts import redirect
from django.db import transaction
from django.db.models import Count, Sum, Q
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from capritools2.models import *
from capritools2.stuff import render_page, random_key
from capritools2.parsers.fleetscanparser import FleetScanParser
from capritools2.tasks import fleet_live_update


def fleet_home(request):
    return render_page(
        "capritools2/fleets.html",
        {},
        request
    )


def fleet_scan_submit(request):
    parser = FleetScanParser()
    if parser.parse(request.POST.get("fleetscan"), request.user):
        return redirect("fleet_scan_view", key=parser.scan.key)
    else:
        request.session['alert_type'] = "danger"
        request.session['alert_message'] = "Failed to parse fleet scan."
        return redirect("fleet")


@login_required
@transaction.atomic
def fleet_live_submit(request):
    pattern = re.compile("/fleets/([0-9]+)/")
    m = pattern.search(request.POST.get("url"))
    if m == None:
        request.session['alert_type'] = "danger"
        request.session['alert_message'] = "Invalid fleet link provided."
        return redirect("fleet")
    fleet_id = m.group(1)

    # Create fleet object
    fleet = Fleet(
        id=fleet_id,
        key=random_key(7),
        user=request.user,
        token = request.user.social_auth.get(provider="eveonline")
    )
    fleet.save()
    fleet_live_update(fleet.id)
    return redirect("fleet_live_view", key=fleet.key)


def fleet_live_monolith(request, key):
    fleet = Fleet.objects.get(key=key)

    supers = [659, 30]
    capitals = [485, 547, 883, 1538] + supers

    # Build JSON object
    out = {
        "id": fleet.id,
        "active": fleet.active,
        "motd": fleet.motd,
        "voice_enabled": fleet.voice_enabled,
        "registered": fleet.registered,
        "free_move": fleet.free_move,
        "members": map(lambda x: x.export(), fleet.members.all()),
        "member_count": fleet.members.count(),
        "commander": fleet.commander(),
        "wings": map(lambda x: x.export(), fleet.wings.all()),
        "member_events": map(lambda x: x.export(character=True), fleet.events.order_by('-timestamp').all()[:100]),
        "ship_changes": map(lambda x: x.export(character=True), fleet.ship_changes.order_by('-timestamp').all()[:100]),
        "jumps": map(lambda x: x.export(character=True), fleet.jumps.order_by('-timestamp').all()[:100]),
        "subs": map(lambda x: dict(x.export().items() + {"ships": x.ships}.items()), Group.objects.filter(
            items__fleet_members__fleet=fleet
        ).exclude(
            id__in=capitals
        ).annotate(
            ships=Count('items')
        ).all()),
        "sub_count": fleet.members.exclude(ship__group_id__in=capitals).count(),
        "caps": map(lambda x: dict(x.export().items() + {"ships": x.ships}.items()), Group.objects.filter(
            items__fleet_members__fleet=fleet,
            id__in=capitals
        ).annotate(
            ships=Count('items')
        ).all()),
        "cap_count": fleet.members.filter(ship__group_id__in=capitals).count(),
        "ships": map(lambda x: dict(x.export().items() + {"ships": x.ships}.items()), Item.objects.filter(
            fleet_members__fleet=fleet
        ).annotate(
            ships=Count('fleet_members')
        ).all()),
        "systems": map(lambda x: dict(x.export().items() + {"members": x.members}.items()), System.objects.filter(
            fleet_members__fleet=fleet
        ).annotate(
            members=Count('fleet_members')
        ).all()),
        "alliances": map(lambda x: dict(x.export().items() + {"members": x.members}.items()), Alliance.objects.filter(
            fleet_members__fleet=fleet
        ).annotate(
            members=Count('fleet_members')
        ).all()),
        "corps": map(lambda x: dict(x.export().items() + {"members": x.members}.items()), Corporation.objects.filter(
            fleet_members__fleet=fleet
        ).annotate(
            members=Count('fleet_members')
        ).all())
    }

    return HttpResponse(json.dumps(out), content_type="application/json")


def fleet_live_memberhistory(request, key):
    fleet = Fleet.objects.get(key=key)
    out = map(lambda x: x.export(character=True), fleet.events.order_by('timestamp').all())
    return HttpResponse(json.dumps(out), content_type="application/json")


def fleet_live_jumphistory(request, key):
    fleet = Fleet.objects.get(key=key)
    out = map(lambda x: x.export(character=True), fleet.jumps.order_by('timestamp').all())
    return HttpResponse(json.dumps(out), content_type="application/json")


def fleet_live_view(request, key):
    fleet = Fleet.objects.get(key=key)

    return render_page(
        "capritools2/fleet_live_view.html",
        {
            "fleet": fleet
        },
        request
    )


def fleet_scan_view(request, key):
    try:
        fleet = FleetScan.objects.get(key=key)

        supers = [659, 30]
        capitals = [485, 547, 883, 1538] + supers

        return render_page(
            "capritools2/fleet_scan_view.html",
            {
                'fleet': fleet,

                'ship_count': Item.objects.filter(
                    fleetMembers__scan=fleet
                ).count(),
                'ships': Item.objects.filter(
                    fleetMembers__scan=fleet
                ).annotate(
                    ships=Count('fleetMembers')
                ).order_by(
                    '-ships'
                ).all(),

                'sub_count': fleet.members.filter(
                        ship__group__category_id=6
                    ).exclude(
                        ship__group_id__in=capitals
                    ).count(),
                'subs': Group.objects.filter(
                        items__fleetMembers__scan=fleet,
                        category_id=6
                    ).exclude(
                        id__in=capitals
                    ).annotate(
                        ships=Count('items')
                    ).order_by(
                        '-ships'
                    ).all(),

                'cap_count': fleet.members.filter(
                        ship__group__category_id=6,
                        ship__group_id__in=capitals
                    ).count(),
                'caps': Group.objects.filter(
                        items__fleetMembers__scan=fleet,
                        category_id=6,
                        id__in=capitals
                    ).annotate(
                        ships=Count('items')
                    ).order_by(
                        '-ships'
                    ).all(),

                'alliances': Alliance.objects.filter(
                    fleetMembers__scan=fleet
                ).annotate(
                    members=Count('fleetMembers')
                ).order_by(
                    '-members'
                ).all(),

                'corps': Corporation.objects.filter(
                    fleetMembers__scan=fleet
                ).annotate(
                    members=Count('fleetMembers')
                ).order_by(
                    '-members'
                ).all(),

                'systems': System.objects.filter(
                    fleetMembers__scan=fleet
                ).annotate(
                    members=Count('fleetMembers')
                ).order_by(
                    '-members'
                ).all()
            },
            request
        )

    except Exception:
        request.session['alert_type'] = "danger"
        request.session['alert_message'] = "Fleet scan %s doesn't exist." % key
        return redirect("fleet")
