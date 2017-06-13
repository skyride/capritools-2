from django.db import models

from capritools2.models import *


class Fleet_Member(models.Model):
    # Fleet
    fleet = models.ForeignKey(Fleet, related_name="members")
    wing = models.ForeignKey(Fleet_Wing, related_name="members", null=True)
    squad = models.ForeignKey(Fleet_Squad, related_name="members", null=True)

    # Character
    character = models.ForeignKey(Character, related_name="fleet_members")
    corporation = models.ForeignKey(Corporation, null=True, related_name="fleet_members")
    alliance = models.ForeignKey(Alliance, null=True, default=None, related_name="fleet_members")

    # Meta
    system = models.ForeignKey(System, related_name="fleet_members", null=True)
    ship = models.ForeignKey(Item, related_name="fleet_members", null=True)
    takes_fleet_warp = models.BooleanField()
    boss = models.BooleanField(default=False)
    role = models.CharField(max_length=16)
    role_name = models.TextField()
    join_time = models.DateTimeField(auto_now_add=True)
