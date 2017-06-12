from django.db import models


class Character(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64, null=True, default=None, db_index=True)

    def __unicode__(self):
        return "id=%s, name=%s" % (self.id, self.name)


    @staticmethod
    def get_or_create(id, name):
        character = Character.objects.filter(id=id)
        if character.count() == 0:
            character = Character(
                id=id,
                name=name
            )
            character.save()
            return character
        else:
            return character[0]


    @staticmethod
    def get_or_create_async(id):
        from capritools2.tasks import fetch_character_info

        character = Character.objects.filter(id=id)
        if character.count() == 1:
            return character[0]

        character = Character(id=id)
        character.save()
        fetch_character_info.delay(id)
        return character
