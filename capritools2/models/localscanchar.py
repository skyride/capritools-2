from django.db import models

from localscan import LocalScan
from character import Character
from corporation import Corporation
from alliance import Alliance
from faction import Faction


class LocalScanChar(models.Model):
    scan = models.ForeignKey(LocalScan, related_name="characters")
    character = models.ForeignKey(Character)
    corporation = models.ForeignKey(Corporation)
    alliance = models.ForeignKey(Alliance, null=True)
    faction = models.ForeignKey(Faction, null=True)
