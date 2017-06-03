import json

from django.db import models

from category import Category


class Group(models.Model):
    id = models.IntegerField(primary_key=True)
    category = models.ForeignKey(Category, related_name="groups")
    name = models.CharField(max_length=100)
    icon = models.IntegerField(null=True)
    published = models.BooleanField()

    def item_ids(self):
        r = self.items.values_list('id', flat=True)
        if r.count() > 0:
            return json.dumps(list(r))
        else:
            return "[]"
