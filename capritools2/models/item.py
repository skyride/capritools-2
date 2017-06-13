from django.db import models
from django.conf import settings
from django.core.cache import cache

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


    def group_class(self):
        if self.group_id in settings.DSCAN_HIGHLIGHTS:
            return "text-%s" % settings.DSCAN_HIGHLIGHTS[self.group_id]


    def __unicode__(self):
        return "id=%s name='%s'" % (self.id, self.name)


    def export(self):
        key = "item_%s" % self.id
        out = cache.get(key)
        if out != None:
            return out
        out = {
            "id": self.id,
            "name": self.name,
            "group": {
                "id": self.group_id,
                "name": self.group.name,
                "category": {
                    "id": self.group.category_id,
                    "name": self.group.category.name
                }
            }
        }

        cache.set(key, out, 3600)
        return out
