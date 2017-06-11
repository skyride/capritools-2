from django.db import models

from capritools2.models import *


class Fleet_Wing(models.Model):
    id = models.IntegerField(primary_key=True)
    fleet = models.ForeignKey(Fleet, related_name="wings")
    name = models.CharField(max_length=10)
