import json

from django.db import models


class Alliance(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64, null=True)
    ticker = models.CharField(max_length=5, null=True, default=None, db_index=True)


    def __unicode__(self):
        return "id=%s name=%s" % (self.id, self.name)


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

    def export(self):
        return {
            "id": self.id,
            "name": self.name,
            "dotlan": self.dotlan_link()
        }


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
            r = api.get("/v3/alliances/%s/" % id)
            alliance = Alliance(
                id=id,
                name=r['name'],
                ticker=r['ticker']
            )
            alliance.save()
            return alliance
        else:
            return alliance[0]


    @staticmethod
    def get_or_create_async(id):
        from capritools2.tasks import fetch_alliance_info

        alliance = Alliance.objects.filter(id=id)
        if alliance.count() == 1:
            return alliance[0]

        alliance = Alliance(id=id)
        alliance.save()
        fetch_alliance_info.delay(id)
        return alliance
