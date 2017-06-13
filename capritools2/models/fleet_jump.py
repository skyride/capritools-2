from django.db import models

from capritools2.models import *


class Fleet_Jump(models.Model):
    fleet = models.ForeignKey(Fleet)
    character = models.ForeignKey(Character)
    from_system = models.ForeignKey(System, related_name="from_system")
    to_system = models.ForeignKey(System, related_name="to_system")
    timestamp = models.DateTimeField(auto_now_add=True)
