import json

from django.db import models
from django.conf import settings

from category import Category


class Group(models.Model):
    id = models.IntegerField(primary_key=True)
    category = models.ForeignKey(Category, related_name="groups")
    name = models.CharField(max_length=100)
    icon = models.IntegerField(null=True)
    published = models.BooleanField()


    def __str__(self):
        return "id=%s name=%s" % (self.id, self.name)


    def item_ids(self):
        r = self.items.values_list('id', flat=True)
        if r.count() > 0:
            return json.dumps(list(r))
        else:
            return "[]"


    def style(self):
        if self.id in settings.DSCAN_HIGHLIGHTS:
            return settings.DSCAN_HIGHLIGHTS[self.id]
        else:
            return "active"


    def export(self):
        return {
            "id": self.id,
            "name": self.name,
            "style": self.style()
        }
