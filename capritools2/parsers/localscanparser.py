import eveapi
import json

from sets import Set

from django.db import transaction

from capritools2.models import *
from capritools2.stuff import random_key
from capritools2.esi import ESI


class LocalScanParser:
    scan = None
    api = ESI()

    def __init__(self):
        eveapi.set_user_agent("eveapi.py/1.3")
        self.xmlapi = eveapi.EVEAPIConnection()


    def parse(self, input):
        # Create initial anchor key
        self.scan = LocalScan(key=random_key(7))
        self.scan.save()

        # Hit the API for characterIDs
        affiliations = Set()
        charAffiliations = []
        names=input.split("\r\n")
    #try:
        for chunk in [names[x:x+100] for x in xrange(0, len(names), 100)]:
            get_vars = {
                "search": ",".join(map(str, chunk)),
                "categories": [
                    "character"
                ]
            }
            r = self.api.get("/search/", get_vars=get_vars)
            print r
            ids = map(lambda x: x['character_id'], r)
            charAffiliations = charAffiliations + self.api.post("/characters/affiliation/", data=json.dumps(ids))
    #except Exception:
        #return False

        # Parse results
        added = 0
        if charAffiliations == None:
            self.scan.delete()
            return False

        for i, affiliation in enumerate(charAffiliations):
            # Populate and retrieve objects in the DB
            char = LocalScanChar(scan=self.scan)
            char.corporation = Corporation.get_or_create(affiliation['corporation_id'])
            if "alliance_id" in affiliation:
                char.alliance = Alliance.get_or_create(affiliation['alliance_id'])
                affiliations.add((affiliation['corporation_id'], affiliation['alliance_id']))
            if "faction_id" in affiliation:
                char.faction = Faction.get_or_create(affiliation['faction_id'])

            added += 1
            char.save()

        for corp_id, alliance_id in affiliations:
            db_affiliation = Affiliation(
                scan=self.scan,
                corporation_id=corp_id,
                alliance_id=alliance_id
            )
            db_affiliation.save()

        if added > 0:
            return True
        else:
            self.scan.save()
            return False
