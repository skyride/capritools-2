import os
import time
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'capritools.settings'
import django
django.setup()

from django.db import connections, transaction
from django.db.utils import IntegrityError

from capritools2.models import *


def time_func(text, f):
    start = time.time()
    print '=> %s:' % text,
    sys.stdout.flush()

    added = f()

    print '%d (%0.2fs)' % (added, time.time() - start)


class Importer:
    def __init__(self):
        self.cursor = connections['import'].cursor()


    def import_all(self):
        time_func('MarketGroup', self.import_marketgroup)
        time_func('Category', self.import_category)
        time_func('Group', self.import_group)
        time_func('Item', self.import_item)
        time_func('Region', self.import_region)
        time_func('Constellation', self.import_constellation)
        time_func('System', self.import_system)


    @transaction.atomic
    def import_system(self):
        added = 0

        self.cursor.execute(
            """
            SELECT
                "solarSystemID", "constellationID", "regionID", "solarSystemName",
                x, y, z, "factionID", radius, "sunTypeID"
            FROM "mapSolarSystems"
            """
        )

        for row in self.cursor:
            db_system = Region.objects.filter(id=row[0])
            if len(db_system) == 0:
                db_system = System(
                    id=row[0]
                )
                added += 1
            else:
                db_system = db_system[0]

            db_system.constellation_id = row[1]
            db_system.region_id = row[2]
            db_system.name = row[3]
            db_system.x = row[4]
            db_system.y = row[5]
            db_system.z = row[6]
            db_system.factionID = row[7]
            db_system.radius = row[8]
            db_system.sun_id = row[9]
            db_system.save()

        return added


    @transaction.atomic
    def import_constellation(self):
        added = 0

        self.cursor.execute(
            """
            SELECT
                "constellationID", "regionID", "constellationName",
                x, y, z, "factionID", radius
            FROM "mapConstellations"
            """
        )

        for row in self.cursor:
            db_constellation = Constellation.objects.filter(id=row[0])
            if len(db_constellation) == 0:
                db_constellation = Constellation(
                    id=row[0]
                )
                added += 1
            else:
                db_constellation = db_constellation[0]

            db_constellation.region_id = row[1]
            db_constellation.name = row[2]
            db_constellation.x = row[3]
            db_constellation.y = row[4]
            db_constellation.z = row[5]
            db_constellation.factionID = row[6]
            db_constellation.radius = row[7]
            db_constellation.save()

        return added


    @transaction.atomic
    def import_region(self):
        added = 0

        self.cursor.execute(
            """
            SELECT
                "regionID", "regionName", x, y, z, "factionID", radius
            FROM "mapRegions"
            """
        )

        for row in self.cursor:
            db_region = Region.objects.filter(id=row[0])
            if len(db_region) == 0:
                db_region = Region(
                    id=row[0]
                )
                added += 1
            else:
                db_region = db_region[0]

            db_region.name = row[1]
            db_region.x = row[2]
            db_region.y = row[3]
            db_region.z = row[4]
            db_region.factionID = row[5]
            db_region.radius = row[6]
            db_region.save()

        return added


    @transaction.atomic
    def import_item(self):
        added = 0

        self.cursor.execute(
            """
            SELECT
                "typeID", "groupID", "typeName", description, mass, volume, capacity, "raceID",
                published, "marketGroupID", "iconID"
            FROM "invTypes"
            """
        )
        # Get group ids for integrity check
        group_ids = set(Group.objects.values_list('id', flat=True))

        for row in self.cursor:
            db_item = Item.objects.filter(id=row[0])
            if len(db_item) == 0:
                db_item = Item(
                    id=row[0]
                )
                added += 1
            else:
                db_item = db_item[0]

            if row[1] in group_ids:
                db_item.group_id = row[1]
                db_item.name = row[2]
                db_item.description = row[3]
                db_item.mass = row[4]
                db_item.volume = row[5]
                db_item.capacity = row[6]
                db_item.raceID = row[7]
                db_item.published = row[8]
                db_item.marketGroup_id = row[9]
                db_item.icon = row[10]
                db_item.save()

        return added


    @transaction.atomic
    def import_marketgroup(self):
        added = 0

        query = """
        SELECT
            "marketGroupID", "parentGroupID", "marketGroupName", description, "iconID", "hasTypes"
        FROM "invMarketGroups"
        ORDER BY "hasTypes", "parentGroupID", "marketGroupID"
        """

        # Add new market groups
        self.cursor.execute(query)
        for row in self.cursor:
            db_marketgroup = MarketGroup.objects.filter(id=row[0])
            if len(db_marketgroup) == 0:
                db_marketgroup = MarketGroup(
                    id=row[0]
                )
                added += 1
                db_marketgroup.save()

        # Update data
        self.cursor.execute(query)
        for row in self.cursor:
            db_marketgroup = MarketGroup.objects.get(id=row[0])

            db_marketgroup.parentGroup_id = row[1]
            db_marketgroup.name = row[2]
            db_marketgroup.description = row[3]
            db_marketgroup.icon = row[4]
            db_marketgroup.hasTypes = row[5]
            db_marketgroup.save()


        return added


    @transaction.atomic
    def import_group(self):
        added = 0

        self.cursor.execute(
            """
            SELECT
                "groupID", "categoryID", "groupName", "iconID", published
            FROM "invGroups"
            """
        )

        for row in self.cursor:
            db_group = Group.objects.filter(id=row[0])
            if len(db_group) == 0:
                db_group = Group(
                    id=row[0]
                )
                added +=1
            else:
                db_group = db_group[0]

            db_group.category_id = row[1]
            db_group.name = row[2]
            db_group.icon = row[3]
            db_group.published = row[4]
            db_group.save()

        return added


    @transaction.atomic
    def import_category(self):
        added = 0

        self.cursor.execute(
            """
            SELECT
                "categoryID", "categoryName", "iconID", published
            FROM "invCategories"
            """
        )

        for row in self.cursor:
            db_category = Category.objects.filter(id=row[0])
            if len(db_category) == 0:
                db_category = Category(
                    id=row[0]
                )
                added += 1
            else:
                db_category = db_category[0]

            db_category.name = row[1]
            db_category.icon = row[2]
            db_category.published = row[3]
            db_category.save()

        return added


importer = Importer()
importer.import_all()
