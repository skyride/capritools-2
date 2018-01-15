from django.db import models


class Faction(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)


    @staticmethod
    def get_or_create(id):
        from capritools2.esi import ESI

        faction = Faction.objects.filter(id=id)
        if faction.count() == 0:
            api = ESI()
            factions = api.get("/v2/universe/factions/")
            faction = filter(lambda x: x['faction_id'] == id, factions)[0]
            faction = Faction(
                id=faction['faction_id'],
                name=faction['name']
            )
            faction.save()
            return faction
        else:
            return faction[0]
