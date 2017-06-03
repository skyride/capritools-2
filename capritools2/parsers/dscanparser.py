import re
from locale import *

from django.db import transaction

from capritools2.models import Dscan, DscanObject, System, Item
from capritools2.stuff import random_key


class DscanParser:
    scan = None
    pattern = re.compile(r"(?P<type_id>\d+)\t(?P<name>.+)\t(?P<type_name>.+)\t((?P<distance>[\d,\.]+) (?P<unit>m|km|AU)|(?P<unknown_distance>-))")
    oldPattern = re.compile(r"(?P<name>.+)\t(?P<type_name>.+)\t((?P<distance>[\d,\.]+) (?P<unit>m|km|AU)|(?P<unknown_distance>-))")
    sunPattern = re.compile(r"(.+) - Star")
    planetPattern = re.compile(r"(.+) [IVX]+")
    moonPattern = re.compile(r"(.+) [IVX]+")
    beltPattern = re.compile(r"(.+) [IVX]+")
    stationPattern = re.compile(r"(.+) [IVX]+")
    structurePattern = re.compile(r"(.+) - ")

    def __init__(self):
        self.item_map = {}
        for id, name in Item.objects.values_list('id', 'name').all():
            self.item_map[name] = id


    # Parse a scan
    @transaction.atomic
    def parse(self, raw, oldFormat=False, key=None, added=None):
        if key == None:
            key = random_key(7)
        self.scan = Dscan(key=key)
        if added != None:
            self.scan.added = added
        self.scan.save()
        lines = raw.splitlines()

        objects = []
        for line in lines:
            # Regex parse the line
            if oldFormat == False:
                m = self.pattern.search(line)
            else:
                m = None

            if m == None:
                m = self.oldPattern.search(line)
                if m != None:
                    m = m.groupdict()

                    type_name = m['type_name'].replace("*", "").replace('\xe2\x99\xa6 ', "")
                    try:
                        m['type_id'] = self.item_map[type_name]
                    except KeyError:
                        m = None
            else:
                m = m.groupdict()

            if m != None:
                # Parse the distance
                if m['unit'] == "m":
                    distance = atof(m['distance'].replace(".", ",").replace(",", ""))
                elif m['unit'] == "km":
                    distance = atof(m['distance'].replace(".", ",").replace(",", "")) * 1000
                elif m['unit'] == "AU":
                    distance = atof(m['distance'].replace(",", "")) * 149597870700
                else:
                    distance = None

                objects.append(DscanObject(
                    dscan=self.scan,
                    item_id=m['type_id'],
                    name=m['name'],
                    distance=distance
                ))

        if len(objects) > 0:
            DscanObject.objects.bulk_create(objects)
            system = self.detect_system()
            if system != None:
                self.scan.system = system
                self.scan.save()

            return True
        else:
            self.scan.delete()
            return False


    def detect_system(self):
        # Try sun
        sun = self.scan.scanObjects.filter(item__group_id=6)
        if sun.count() > 0:
            m = self.sunPattern.search(sun[0].name)
            if m != None:
                try:
                    return System.objects.get(name=m.group(1))
                except Exception:
                    pass

        # Try planets
        planets = self.scan.scanObjects.filter(item__group_id=7)
        for planet in planets:
            m = self.planetPattern.search(planet.name)
            if m != None:
                try:
                    return System.objects.get(name=m.group(1))
                except Exception:
                    pass

        # Try moons
        moons = self.scan.scanObjects.filter(item__group_id=8)
        for moon in moons:
            m = self.moonPattern.search(moon.name)
            if m != None:
                try:
                    return System.objects.get(name=m.group(1))
                except Exception:
                    pass

        # Try asteroid belts
        belts = self.scan.scanObjects.filter(item__group_id=9)
        for belt in belts:
            m = self.beltPattern.search(belt.name)
            if m != None:
                try:
                    return System.objects.get(name=m.group(1))
                except Exception:
                    pass

        # Try stations
        stations = self.scan.scanObjects.filter(item__group__category_id=3)
        for station in stations:
            m = self.stationPattern.search(station.name)
            if m != None:
                try:
                    return System.objects.get(name=m.group(1))
                except Exception:
                    pass

        # Try structures
        structures = self.scan.scanObjects.filter(
            item__group__category_id=65
        ).exclude(
            item__group_id__in=[1876]
        )
        for structure in structures:
            m = self.structurePattern.search(structure.name)
            if m != None:
                try:
                    return System.objects.get(name=m.group(1))
                except Exception:
                    pass
