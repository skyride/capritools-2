from django.db import models

from region import Region


class Constellation(models.Model):
    id = models.IntegerField(primary_key=True)
    region = models.ForeignKey(Region)
    name = models.CharField(max_length=100)
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    factionID = models.IntegerField(null=True)
    radius = models.FloatField(null=True)
