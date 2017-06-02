from django.db import models

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
