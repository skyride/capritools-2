from django.db import models


class Corporation(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    ticker = models.CharField(max_length=5)


    @staticmethod
    def get_or_create(id):
        from capritools2.esi import ESI

        corporation = Corporation.objects.filter(id=id)
        if corporation.count() == 0:
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
