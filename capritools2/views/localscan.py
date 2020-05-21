import json

from django.http import HttpResponse
from django.shortcuts import redirect
from django.db.models import Count, Sum, Q
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache

from capritools2.parsers.localscanparser import LocalScanParser
from capritools2.stuff import render_page
from capritools2.models import *


def localscan_home(request):
    return render_page(
        "capritools2/localscan.html",
        {},
        request
    )


def localscan_view(request, key):
    try:
        scan = LocalScan.objects.get(key=key)
        scan_characters_count = scan.characters.count()
    except ObjectDoesNotExist:
        request.session['alert_type'] = "danger"
        request.session['alert_message'] = "The Local Scan you were looking for does not exist."
        return redirect("localscan")

    alliances = Alliance.objects.filter(
        localChars__scan=scan
    ).annotate(
        item_count=Count('localChars')
    ).order_by(
        '-item_count'
    ).all()
    for i, alliance in enumerate(alliances):
        alliance.style = ['info', 'success', 'warning', 'danger'][i % 4]
        alliance.width = (100.0 / scan_characters_count) * alliance.item_count

    corps = Corporation.objects.filter(
        localChars__scan=scan
    ).annotate(
        item_count=Count('localChars')
    ).order_by(
        '-item_count'
    ).all()
    for i, corp in enumerate(corps):
        corp.style = ['info', 'success', 'warning', 'danger'][i % 4]
        corp.width = (100.0 / scan_characters_count) * corp.item_count

    data = {
        'scan': scan,
        'alliances': alliances,
        'corps': corps
    }

    return render_page(
        "capritools2/localscan_view.html",
        data,
        request
    )



def localscan_submit(request):
    parser = LocalScanParser()
    if not parser.parse(request.POST.get("scan")):
        request.session['alert_type'] = "danger"
        request.session['alert_message'] = "Failed to parse Local Scan you entered."
        return redirect("localscan")

    if request.user.is_authenticated():
        parser.scan.user = request.user
        parser.scan.save()

    return redirect("localscan_view", key=parser.scan.key)
