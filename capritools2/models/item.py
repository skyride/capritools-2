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
    buy = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    sell = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    last_updated = models.DateTimeField(null=True)


    def implant_type(self):
        return self.name.split(" ")[-1]


    def __unicode__(self):
        return "id=%s name='%s'" % (self.id, self.name)
