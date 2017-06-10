import json

from django.db import models


class Alliance(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    ticker = models.CharField(max_length=5, null=True, default=None, db_index=True)


    def dotlan_link(self):
        return "http://evemaps.dotlan.net/alliance/%s" % (
            self.name.replace(" ", "_")
        )

    def affiliations(self):
        r = self.localscan_affiliations.values_list('corporation', flat=True)
        if r.count() > 0:
            return json.dumps(list(r)+[self.id])
        else:
            return "[]"


    @staticmethod
    def get_or_create(id, name=None):
        from capritools2.esi import ESI

        if name != None:
            alliance = Alliance(
                id=id,
                name=name
            )
            alliance.save()
            return alliance

        alliance = Alliance.objects.filter(id=id)
        if alliance.count() == 0:
            api = ESI()
            r = api.get("/alliances/%s/" % id)
            alliance = Alliance(
                id=id,
                name=r['alliance_name'],
                ticker=r['ticker']
            )
            alliance.save()
            return alliance
        else:
            return alliance[0]
