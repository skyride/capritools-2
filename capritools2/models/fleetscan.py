from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User

from capritools2.models import System


class FleetScan(models.Model):
    key = models.CharField(max_length=40, unique=True, db_index=True)
    added = models.DateTimeField(auto_now_add=True, db_index=True)
    user = models.ForeignKey(User, null=True, default=None)


    def fleet_command(self):
        try:
            return self.members.get(wing=None)
        except Exception:
            return None


    def main_system(self):
        try:
            return System.objects.filter(
                fleetMembers__scan=self
            ).annotate(
                members=Count('fleetMembers')
            ).order_by(
                '-members'
            ).first()
        except Exception:
            return None
