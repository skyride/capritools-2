import requests
import json

from datetime import datetime, timedelta
from pytz import utc

from django.db import transaction
from django.db.models import Q
from django.core.paginator import Paginator

from capritools import settings
from capritools2.models import Item
from capritools.celery import app


@app.task(name="price_update_spawner")
def price_update_spawner():
    items = Item.objects.filter(
        Q(last_updated__lt=datetime.now(utc) - timedelta(days=1)) | Q(last_updated__isnull=True),
        marketGroup_id__isnull=False
    ).order_by(
        'id'
    ).all()

    if items.count() > 0:
        paginator = Paginator(items, 100)
        for i in paginator.page_range:
            page = paginator.page(i)
            type_ids = map(lambda x: x.id, page)
            fetch_prices.delay(type_ids)

        print "Market Update Spawner called for the update of %s items" % (items.count())
    else:
        print "No market prices to be updated"


@app.task(name="fetch_prices")
@transaction.atomic
def fetch_prices(ids):
    ids = ",".join(map(str, ids))
    url = settings.PRICE_URL % ids
    r = requests.get(url)
    r = json.loads(r.text)

    for item in r:
        db_item = Item.objects.get(id=item['sell']['forQuery']['types'][0])
        db_item.sell = round(item['sell']['fivePercent'], 2)
        db_item.buy = round(item['buy']['fivePercent'], 2)
        db_item.last_updated = datetime.now(utc)
        db_item.save()

    print "Updated prices for %s items" % len(r)
