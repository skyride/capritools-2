from django.db import models

from capritools2.models import *


class Fleet_Wing(models.Model):
    id = models.BigIntegerField(primary_key=True)
    fleet = models.ForeignKey(Fleet, related_name="wings")
    name = models.CharField(max_length=10)


    @staticmethod
    def get_or_create(id, fleet, name):
        try:
            return Fleet_Wing.objects.get(id=id)
        except Exception:
            wing = Fleet_Wing(
                id=id,
                fleet=fleet,
                name=name
            )
            wing.save()
            return wing
