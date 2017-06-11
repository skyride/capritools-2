from django.db import models

from capritools2.models import *


class Fleet(models.Model):
    id = models.IntegerField(primary_key=True)
    motd = models.TextField()
    voice_enabled = models.BooleanField()
    registered = models.BooleanField()
    free_move = models.BooleanField()
