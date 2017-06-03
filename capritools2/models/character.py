

from django.db import models


class Character(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)


    @staticmethod
    def get_or_create(id):
        from capritools2.esi import ESI

        character = Character.objects.filter(id=id)
        if character.count() == 0:
            api = ESI()
            r = api.get("/characters/%s/" % id)
            character = Character(
                id=id,
                name=r['name']
            )
            character.save()
            return character
        else:
            return character[0]
