from django.db import models

from capritools2.models import *


class Fleet_MemberEvent(models.Model):
    fleet = models.ForeignKey(Fleet)
    character = models.ForeignKey(Character)
    event = models.CharField(max_length=16, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True)
