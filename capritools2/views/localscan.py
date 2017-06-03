from django.http import HttpResponse
from django.shortcuts import redirect
from django.db.models import Count, Sum, Q

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
    scan = LocalScan.objects.get(key=key)

    alliances = Alliance.objects.filter(
        localChars__scan=scan
    ).annotate(
        item_count=Count('localChars')
    ).order_by(
        '-item_count'
    )
    for i, alliance in enumerate(alliances):
        alliance.style = ['info', 'success', 'warning', 'danger'][i % 4]
        alliance.width = (float(100) / scan.characters.count()) * alliance.item_count

    corps = Corporation.objects.filter(
        localChars__scan=scan
    ).annotate(
        item_count=Count('localChars')
    ).order_by(
        '-item_count'
    )
    for i, corp in enumerate(corps):
        corp.style = ['info', 'success', 'warning', 'danger'][i % 4]
        corp.width = (float(100) / scan.characters.count()) * corp.item_count

    return render_page(
        "capritools2/localscan_view.html",
        {
            'scan': scan,
            'alliances': alliances,
            'corps': corps
        },
        request
    )



def localscan_submit(request):
    parser = LocalScanParser()
    status = parser.parse(request.POST.get("scan"))
    if status == True:
        return redirect("localscan_view", key=parser.scan.key)
