from django.db import models

from capritools2.models import *


class Fleet_Squad(models.Model):
    id = models.BigIntegerField(primary_key=True)
    fleet = models.ForeignKey(Fleet, related_name="squads")
    wing = models.ForeignKey(Fleet_Wing, related_name="squads")
    name = models.CharField(max_length=10)

    class Meta:
        ordering = ['name']

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


    def commander(self):
        try:
            return self.members.get(role="squad_commander").export()
        except Exception:
            return None


    def export(self):
        return {
            "id": self.id,
            "name": self.name,
            "commander": self.commander(),
            "member_count": self.members.count(),
            "members": map(lambda x: x.export(), self.members.filter(role="squad_member"))
        }
