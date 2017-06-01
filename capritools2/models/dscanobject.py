from django.db import models

from dscan import Dscan
from item import Item


class DscanObject(models.Model):
    dscan = models.ForeignKey(Dscan, related_name="scanObjects")
    item = models.ForeignKey(Item)
    name = models.CharField(max_length=64)
    distance = models.FloatField()