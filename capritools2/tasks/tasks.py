import requests
import json

from datetime import datetime, timedelta
from pytz import utc

from django.db import transaction
from django.db.models import Q
from django.core.paginator import Paginator

from capritools import settings
from capritools2.models import *
from capritools2.esi import ESI
from capritools.celery import app


# The ESI API only provides IDs, use this to fix missing info we don't call for async
@app.task(name="fetch_spawner")
def fetch_spawner():
    for char in Character.objects.filter(name=None).all():
        fetch_character_info(char.id)
    for corp in Corporation.objects.filter(Q(ticker=None) | Q(name=None)).all():
        fetch_corp_info.delay(corp.id)
    for alliance in Alliance.objects.filter(Q(ticker=None) | Q(name=None)).all():
        fetch_alliance_info.delay(alliance.id)


@app.task(name="fetch_character_info")
def fetch_character_info(id):
    api = ESI()
    char = api.get("/v4/characters/%s/" % id)
    db_char = Character.objects.get(id=id)
    db_char.name = char['name']
    db_char.save()
    print "Fetched info for %s:%s" % (db_char.id, db_char.name)


@app.task(name="fetch_corp_info")
def fetch_corp_info(id):
    api = ESI()
    corp = api.get("/v4/corporations/%s/" % id)
    db_corp = Corporation.objects.get(id=id)
    db_corp.name = corp['name']
    db_corp.ticker = corp['ticker']
    db_corp.save()
    print "Fetched info for %s:%s" % (db_corp.id, db_corp.name)


@app.task(name="fetch_alliance_info")
def fetch_alliance_info(id):
    api = ESI()
    alliance = api.get("/v3/alliances/%s/" % id)
    db_alliance = Alliance.objects.get(id=id)
    db_alliance.name = alliance['name']
    db_alliance.ticker = alliance['ticker']
    db_alliance.save()
    print "Fetched info for %s:%s" % (db_alliance.id, db_alliance.name)


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
