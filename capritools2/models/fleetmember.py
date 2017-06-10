from django.db import models
from django.contrib.auth.models import User

from capritools2.models import *


class FleetMember(models.Model):
    scan = models.ForeignKey(FleetScan, related_name="members")

    # Character
    name = models.CharField(max_length=64, db_index=True)
    corporation = models.ForeignKey(Corporation, null=True, default=None, related_name="fleetMembers")
    alliance = models.ForeignKey(Alliance, null=True, default=None, related_name="fleetMembers")
    leadership = models.IntegerField()
    wing_command = models.IntegerField()
    fleet_command = models.IntegerField()

    # Meta
    system = models.ForeignKey(System, related_name="fleetMembers")
    ship = models.ForeignKey(Item, related_name="fleetMembers")

    # Fleet
    command = models.BooleanField(default=False)
    boss = models.BooleanField(default=False)
    wing = models.ForeignKey(FleetWing, null=True, default=None, related_name="members")
    squad = models.ForeignKey(FleetSquad, null=True, default=None, related_name="members")


    def fleet_boss(self):
        if self.boss:
            return "(Boss)"
        else:
            return ""


    def fleet_skills(self):
        return "%s - %s - %s" % (self.fleet_command, self.wing_command, self.leadership)


    class Meta:
        ordering = ['wing', 'squad', 'command', 'name']
