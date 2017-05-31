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
