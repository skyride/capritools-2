from django.db import models

from dscan import Dscan
from item import Item


class DscanObject(models.Model):
    dscan = models.ForeignKey(Dscan, related_name="scanObjects", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name="scanObjects")
    name = models.CharField(max_length=128)
    distance = models.BigIntegerField(null=True)
