import re

from django.shortcuts import redirect
from django.db.models import Count, Sum, Q
from django.http import HttpResponse

from capritools2.models import *
from capritools2.stuff import render_page
from capritools2.parsers.fleetscanparser import FleetScanParser


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


def fleet_live_submit(request):
    pattern = re.compile("https://crest-tq.eveonline.com/fleets/([0-9]+)/")
    m = pattern.search(request.POST.get("url"))
    fleet_id = m.group(1)

    # Create fleet object
    fleet = Fleet(
        id=fleet_id,
        token = request.user.social_auth.get(provider="eveonline")
    )
    fleet.save()
    return HttpResponse(fleet_id)


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
