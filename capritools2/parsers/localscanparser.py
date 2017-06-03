import eveapi
import json

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


    @transaction.atomic
    def parse(self, input):
        # Create initial anchor key
        self.scan = LocalScan(key=random_key(7))
        self.scan.save()

        # Hit the API for characterIDs
        r = self.xmlapi.eve.CharacterID(names=input.replace("\r\n", ","))
        ids = map(lambda x: x.characterID, r.characters)

        # Parse results
        added = 0
        affiliations = self.api.post("/characters/affiliation/", data=json.dumps(ids))
        if affiliations == None:
            self.scan.save()
            return False

        for affiliation in affiliations:
            # Populate and retrieve objects in the DB
            char = LocalScanChar(scan=self.scan)
            char.character = Character.get_or_create(affiliation['character_id'])
            char.corporation = Corporation.get_or_create(affiliation['corporation_id'])
            if "alliance_id" in affiliation:
                char.alliance = Alliance.get_or_create(affiliation['alliance_id'])
            if "faction_id" in affiliation:
                char.faction = Faction.get_or_create(affiliation['faction_id'])

            added += 1
            char.save()

        if added > 0:
            return True
        else:
            self.scan.save()
            return False
