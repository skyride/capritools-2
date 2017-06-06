import json

from django.shortcuts import redirect

from capritools2.stuff import render_page
from capritools2.models import Item
from capritools2.moongoo import towers


def quickmath_home(request):
    return render_page(
        "capritools2/quickmath.html",
        {},
        request
    )



def quickmath_moongoo(request):
    items = [
        16650, 16651, 16652, 16653,     # R64
        16649, 16648, 16647, 16646,     # R32
        16643, 16644, 16642, 16641,     # R16
        16640, 16639, 16638, 16637,     # R8
        16634, 16635, 16633, 16636      # R4
    ]

    minerals = []
    db_items = Item.objects.filter(id__in=items).order_by('-id').all()
    for i, item in enumerate(db_items):
        minerals.append({
            'id': item.id,
            'name': item.name,
            'class': 2 ** (((19 - i) / 4) + 2),
            'sell': float(item.sell),
            'buy': float(item.buy)
        })

    for tower in towers:
        tower['sell'] = float(Item.objects.get(id=tower['id']).sell)

    blocks = []
    for block in Item.objects.filter(id__in=[4247, 4312, 4246, 4051]).all():
        blocks.append({
            'id': block.id,
            'name': block.name,
            'sell': float(block.sell),
            'buy': float(block.buy)
        })

    return render_page(
        "capritools2/moongoo.html",
        {
            'minerals': json.dumps(minerals),
            'towers': json.dumps(towers),
            'blocks': json.dumps(blocks)
        },
        request
    )
