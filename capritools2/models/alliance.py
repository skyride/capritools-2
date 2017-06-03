from django.db import models


class Alliance(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    ticker = models.CharField(max_length=5)


    @staticmethod
    def get_or_create(id):
        from capritools2.esi import ESI

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
