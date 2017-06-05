from django.http import HttpResponse
from django.shortcuts import redirect, reverse
from django.db.models import Count, Sum, Q
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

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
    try:
        scan = Dscan.objects.get(key=key)
    except ObjectDoesNotExist:
        request.session['alert_type'] = "danger"
        request.session['alert_message'] = "The Dscan you were looking for does not exist."
        return redirect("dscan")

    supers = [659, 30]
    capitals = [485, 547, 883, 1538] + supers

    info = scan.scanObjects.filter(
        item__group__category_id=6
    ).exclude(
        item__group_id__in=supers
    ).annotate(
        items_mass=Sum('item__mass'),
        items_volume=Sum('item__volume')
    ).aggregate(
        total_mass=Sum('items_mass'),
        total_volume=Sum('items_volume')
    )

    # Calculate bridge usage
    info['titan_topes'] = info['total_mass'] * 1500 * 0.000000001 * 0.6 * 6
    info['blops_topes'] = info['total_mass'] * 450 * 0.000000135 * 0.6 * 8

    return render_page(
        "capritools2/dscan_view.html",
        {
            'scan': scan,
            'info': info,
            'highlights': None,

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
                ),

            'misc': Group.objects.filter(
                    items__scanObjects__dscan=scan,
                    id__in=settings.DSCAN_MISC_GROUPS
                ).annotate(
                    item_count=Count('items')
                ).order_by(
                    '-item_count'
                ),

            'structures': Group.objects.filter(
                    items__scanObjects__dscan=scan
                ).filter(
                    Q(category_id__in=[65]) | Q(id__in=[365]) | Q()
                ).annotate(
                    item_count=Count('items')
                ).order_by(
                    '-item_count'
                ),
        },
        request
    )


def dscan_submit(request):
    parser = DscanParser()

    if not parser.parse(request.POST.get("dscan")):
        request.session['alert_type'] = "danger"
        request.session['alert_message'] = "Failed to parse Dscan you entered."
        return redirect("dscan")

    return redirect("dscan_view", key=parser.scan.key)
