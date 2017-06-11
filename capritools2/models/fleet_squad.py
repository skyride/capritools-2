from django.db import models

from capritools2.models import *


class Fleet_Squad(models.Model):
    id = models.IntegerField(primary_key=True)
    fleet = models.ForeignKey(Fleet, related_name="squads")
    wing = models.ForeignKey(Fleet_Wing, related_name="squads")
    name = models.CharField(max_length=10)
