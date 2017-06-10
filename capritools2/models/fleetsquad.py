from django.db import models

from capritools2.models import FleetScan, FleetWing


class FleetSquad(models.Model):
    scan = models.ForeignKey(FleetScan, related_name="squads")
    wing = models.ForeignKey(FleetWing, related_name="squads")
    name = models.CharField(max_length=64, db_index=True)

    class Meta:
        ordering = ['name']

    @staticmethod
    def get_or_create(scan, wing, name):
        try:
            return FleetSquad.objects.get(scan=scan, wing=wing, name=name)
        except Exception:
            obj = FleetSquad(scan=scan, wing=wing, name=name)
            obj.save()
            return obj


    def squad_command(self):
        try:
            return self.members.get(command=True)
        except Exception:
            return None


    def squadies(self):
        try:
            return self.members.filter(command=False).all()
        except Exception:
            return []
