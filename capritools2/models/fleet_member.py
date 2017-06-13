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


    class Meta:
        ordering = ['character__name']


    def export(self):
        from capritools2.models import *
        t = {
            "id": self.id,
            "takes_fleet_warp": self.takes_fleet_warp,
            "boss": self.boss,
            "role": self.role,
            "role_name": self.role_name,
            "fleet": {},
            "character": self.character.export(),
            "ship": self.ship.export(),
            "location": self.system.export(),
        }

        if self.corporation != None:
            t['corporation'] = {
                "id": self.corporation_id,
                "name": self.corporation.name
            }
        if self.alliance != None:
            t['alliance'] = {
                "id": self.alliance_id,
                "name": self.alliance.name
            }
        if self.wing != None:
            t['fleet']['wing'] = {
                "id": self.wing_id,
                "name": self.wing.name
            }
        if self.squad != None:
            t['fleet']['squad'] = {
                "id": self.squad_id,
                "name": self.squad.name
            }
        return t
