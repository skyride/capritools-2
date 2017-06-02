from django.db import models

from group import Group
from marketgroup import MarketGroup

class Item(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(Group, related_name="items")
    name = models.CharField(max_length=100)
    description = models.TextField()
    mass = models.FloatField()
    volume = models.FloatField()
    capacity = models.FloatField()
    raceID = models.IntegerField(null=True)
    published = models.BooleanField()
    marketGroup = models.ForeignKey(MarketGroup, null=True)
    icon = models.IntegerField(null=True)
