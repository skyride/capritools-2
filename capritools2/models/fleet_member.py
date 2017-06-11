from django.db import models

from capritools2.models import *


class Fleet_Member(models.Model):
    # Fleet
    fleet = models.ForeignKey(Fleet, related_name="members")
    wing = models.ForeignKey(Fleet_Wing, related_name="members")
    squad = models.ForeignKey(Fleet_Squad, related_name="members")

    # Character
    character = models.ForeignKey(Character, related_name="fleet_members")
    corporation = models.ForeignKey(Corporation, related_name="fleet_members")
    alliance = models.ForeignKey(Alliance, null=True, default=None, related_name="fleet_members")

    # Meta
    system = models.ForeignKey(System, related_name="fleet_members")
    ship = models.ForeignKey(Item, related_name="fleet_members")
    takes_fleet_warp = models.BooleanField()
    role = models.CharField(max_length=16)
    role_name = models.TextField()
    join_time = models.DateTimeField()
