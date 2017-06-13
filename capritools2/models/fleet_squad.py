from django.db import models

from capritools2.models import *


class Fleet_Squad(models.Model):
    id = models.BigIntegerField(primary_key=True)
    fleet = models.ForeignKey(Fleet, related_name="squads")
    wing = models.ForeignKey(Fleet_Wing, related_name="squads")
    name = models.CharField(max_length=10)

    @staticmethod
    def get_or_create(id, fleet, wing, name):
        try:
            return Fleet_Squad.objects.get(id=id)
        except Exception:
            squad = Fleet_Squad(
                id=id,
                fleet=fleet,
                wing=wing,
                name=name
            )
            squad.save()
            return squad
