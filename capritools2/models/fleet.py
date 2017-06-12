from django.db import models

from social_django.models import UserSocialAuth

from capritools2.models import *
from capritools2.esi import ESI


class Fleet(models.Model):
    id = models.IntegerField(primary_key=True)
    token = models.ForeignKey(UserSocialAuth)
    active = models.BooleanField(default=True, db_index=True)
    motd = models.TextField()
    voice_enabled = models.BooleanField()
    registered = models.BooleanField()
    free_move = models.BooleanField()
