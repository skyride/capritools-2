from django.http import HttpResponse
from django.shortcuts import redirect, reverse
from django.db.models import Count, Sum

from capritools2.models import Dscan, Group, Item
from capritools2.stuff import render_page
from capritools2.parsers.dscanparser import DscanParser


def dscan_home(request):
    return render_page(
        "capritools2/dscan.html",
        {},
        request
    )


def dscan_view(request, key):
    scan = Dscan.objects.get(key=key)

    capitals = [7, 485, 547, 659, 883, 1538]

    return render_page(
        "capritools2/dscan_view.html",
        {
            'scan': scan,
            'ship_count': scan.scanObjects.filter(item__group__category_id=6).count(),
            'ships': Item.objects.filter(
                    group__category_id=6,
                    scanObjects__dscan=scan
                ).annotate(
                    ships=Count('scanObjects')
                ).order_by(
                    '-ships'
                ),

            'sub_count': scan.scanObjects.filter(
                    item__group__category_id=6
                ).exclude(
                    item__group_id__in=capitals
                ).count(),
            'subs': Group.objects.filter(
                    category_id=6,
                    items__scanObjects__dscan=scan
                ).exclude(
                    items__group_id__in=capitals
                ).annotate(
                    ships=Count('items')
                ).order_by(
                    '-ships'
                ),

            'cap_count': scan.scanObjects.filter(
                    item__group__category_id=6,
                    item__group_id__in=capitals
                ).count(),
            'caps': Group.objects.filter(
                    category_id=6,
                    items__scanObjects__dscan=scan,
                    items__group_id__in=capitals
                ).annotate(
                    ships=Count('items')
                ).order_by(
                    '-ships'
                )
        },
        request
    )


def dscan_submit(request):
    parser = DscanParser()
    parser.parse(request.POST.get("dscan"))
    return redirect("dscan_view", key=parser.scan.key)
