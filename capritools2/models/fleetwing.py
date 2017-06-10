from django.db import models

from capritools2.models import FleetScan


class FleetWing(models.Model):
    scan = models.ForeignKey(FleetScan, related_name="wings")
    name = models.CharField(max_length=64, db_index=True)

    class Meta:
        ordering = ['name']


    @staticmethod
    def get_or_create(scan, name):
        try:
            return FleetWing.objects.get(scan=scan, name=name)
        except Exception:
            obj = FleetWing(scan=scan, name=name)
            obj.save()
            return obj


    def wing_command(self):
        try:
            return self.members.get(squad=None)
        except Exception:
            return None
