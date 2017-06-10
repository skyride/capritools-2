import json

from django.db import models


class Corporation(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    ticker = models.CharField(max_length=5, null=True, default=None, db_index=True)


    def dotlan_link(self):
        return "http://evemaps.dotlan.net/corp/%s" % (
            self.name.replace(" ", "_")
        )

    def affiliations(self):
        r = self.localscan_affiliations.values_list('alliance', flat=True)
        if r.count() > 0:
            return json.dumps(list(r)+[self.id])
        else:
            return "[]"


    @staticmethod
    def get_or_create(id, name=None):
        from capritools2.esi import ESI

        corporation = Corporation.objects.filter(id=id)
        if corporation.count() == 0:
            if name != None:
                corporation = Corporation(
                    id=id,
                    name=name
                )
                corporation.save()
                return corporation

            api = ESI()
            r = api.get("/corporations/%s/" % id)
            corporation = Corporation(
                id=id,
                name=r['corporation_name'],
                ticker=r['ticker']
            )
            corporation.save()
            return corporation
        else:
            return corporation[0]
