from django.db import models

from localscan import LocalScan
from corporation import Corporation
from alliance import Alliance


class Affiliation(models.Model):
    scan = models.ForeignKey(LocalScan, related_name="affiliations")
    corporation = models.ForeignKey(Corporation, db_index=True, related_name="localscan_affiliations")
    alliance = models.ForeignKey(Alliance, db_index=True, related_name="localscan_affiliations")

    class Meta:
        unique_together = ('scan', 'corporation', 'alliance')
