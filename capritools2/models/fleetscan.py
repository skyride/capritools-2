from django.db import models
from django.contrib.auth.models import User


class FleetScan(models.Model):
    key = models.CharField(max_length=40, unique=True, db_index=True)
    added = models.DateTimeField(auto_now_add=True, db_index=True)
    user = models.ForeignKey(User, null=True, default=None)


    def fleet_command(self):
        try:
            return self.members.get(wing=None)
        except Exception:
            return None
