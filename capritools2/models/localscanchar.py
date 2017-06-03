from django.db import models

from character import Character
from corporation import Corporation
from alliance import Alliance
from localscan import LocalScan


class LocalScanChar(models.Model):
    scan = models.ForeignKey(LocalScan, related_name="characters")
    character = models.ForeignKey(Character)
    corporation = models.ForeignKey(Corporation)
    alliance = models.ForeignKey(Alliance, null=True)
