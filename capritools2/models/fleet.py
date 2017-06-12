from django.db import models
from django.contrib.auth.models import User

from social_django.models import UserSocialAuth

from capritools2.esi import ESI


class Fleet(models.Model):
    id = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey(User)
    token = models.ForeignKey(UserSocialAuth)
    active = models.BooleanField(default=True, db_index=True)
    motd = models.TextField(null=True)
    voice_enabled = models.NullBooleanField()
    registered = models.NullBooleanField()
    free_move = models.NullBooleanField()

    def __unicode__(self):
        return "id=%s" % self.id
