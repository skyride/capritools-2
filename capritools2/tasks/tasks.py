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


@app.task
def update_prices():
    api = ESI()
    prices = api.get("/v1/markets/prices/")

    # Transform to a type ID map
    prices = {
        price['type_id']: price
        for price in prices}

    # Update item ids
    with transaction.atomic():
        for type_id, data in prices.items():
            updated = Item.objects.filter(id=type_id).update(
                buy=data['adjusted_price'],
                sell=data['adjusted_price'])

            if updated < 1:
                print "No item for ID %s" % type_id

        print "Updated prices for %s items" % len(prices)
