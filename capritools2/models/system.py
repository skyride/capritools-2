from django.db import models
from django.core.cache import cache

from item import Item
from region import Region
from constellation import Constellation


class System(models.Model):
    id = models.IntegerField(primary_key=True)
    constellation = models.ForeignKey(Constellation)
    region = models.ForeignKey(Region)
    name = models.CharField(max_length=100, db_index=True)
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    factionID = models.IntegerField(null=True)
    radius = models.FloatField(null=True)
    sun = models.ForeignKey(Item)


    def dotlan_system(self):
        return "https://evemaps.dotlan.net/map/%s/%s" % (
            self.region.name.replace(" ", "_"),
            self.name.replace(" ", "_")
        )


    def dotlan_constellation(self):
        return "https://evemaps.dotlan.net/map/%s/%s" % (
            self.region.name.replace(" ", "_"),
            self.constellation.name.replace(" ", "_")
        )


    def dotlan_region(self):
        return "https://evemaps.dotlan.net/map/%s" % (
            self.region.name.replace(" ", "_")
        )

    def export(self):
        key = "system__%s" % self.id
        out = cache.get(key)
        if out != None:
            return out

        out = {
            "system": {
                "id": self.id,
                "name": self.name,
                "sun_type": self.sun_id
            },
            "constellation": {
                "id": self.constellation_id,
                "name": self.constellation.name
            },
            "region": {
                "id": self.region_id,
                "name": self.region.name
            }
        }
        cache.set(key, out, 3600)
        return out
