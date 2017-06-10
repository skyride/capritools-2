import re
import eveapi
from locale import *

from django.db import transaction

from capritools2.models import *
from capritools2.stuff import random_key
from capritools2.esi import ESI


class FleetScanParser:
    scan = None
    positionPattern = re.compile(r"(?P<wing>.+) / (?P<squad>.+)")
    skillsPattern = re.compile(r'(?P<fleet>[0-5]) - (?P<wing>[0-5]) - (?P<leadership>[0-5])')

    def __init__(self):
        eveapi.set_user_agent("eveapi.py/1.3")
        self.xmlapi = eveapi.EVEAPIConnection()


    @transaction.atomic
    def parse(self, raw, user):
        lines = raw.splitlines()

        try:
            if len(lines):
                lines = map(lambda x: x.split("\t"), lines)
                self.scan = FleetScan(key=random_key(7))

                if user.is_authenticated():
                    self.scan.user = user
                self.scan.save()

                # Get corp and alliance
                r = self.xmlapi.eve.CharacterID(names=",".join(map(lambda x: x[0], lines)))
                r = self.xmlapi.eve.CharacterAffiliation(ids=",".join(map(lambda x: str(x.characterID), r.characters)))
                fleetEntries = []
                for affiliation in r.characters:
                    fleetEntries.append((affiliation, filter(lambda x: x[0] == affiliation.characterName, lines)[0]))

                for affiliation, line in fleetEntries:
                    if line[4].startswith("Fleet Commander"):
                        wing = None
                        squad = None
                        command = True

                    if line[4].startswith("Wing Commander"):
                        wing = FleetWing.get_or_create(scan=self.scan, name=line[6])
                        squad = None
                        command = True

                    if line[4].startswith("Squad Commander"):
                        m = self.positionPattern.search(line[6]).groupdict()
                        wing = FleetWing.get_or_create(scan=self.scan, name=m['wing'])
                        squad = FleetSquad.get_or_create(scan=self.scan, wing=wing, name=m['squad'])
                        command = True

                    if line[4].startswith("Squad Member"):
                        m = self.positionPattern.search(line[6]).groupdict()
                        wing = FleetWing.get_or_create(scan=self.scan, name=m['wing'])
                        squad = FleetSquad.get_or_create(scan=self.scan, wing=wing, name=m['squad'])
                        command = False

                    if affiliation.allianceID > 0:
                        alliance = Alliance.get_or_create(affiliation.allianceID, name=affiliation.allianceName)
                    else:
                        alliance = None

                    skills = self.skillsPattern.search(line[5]).groupdict()

                    member = FleetMember(
                        scan=self.scan,

                        name=line[0],
                        corporation=Corporation.get_or_create(affiliation.corporationID, name=affiliation.corporationName),
                        alliance=alliance,
                        leadership=skills['leadership'],
                        wing_command=skills['wing'],
                        fleet_command=skills['fleet'],

                        system=System.objects.get(name=line[1]),
                        ship=Item.objects.get(name=line[2]),

                        command=command,
                        boss="(Boss)" in line[4],
                        wing=wing,
                        squad=squad
                    )
                    member.save()

                return True

            else:
                try:
                    self.scan.delete()
                except Exception:
                    pass

                return False


        except Exception:
            return False
