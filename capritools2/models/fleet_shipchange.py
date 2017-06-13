from django.db import models

from capritools2.models import *


class Fleet_ShipChange(models.Model):
    fleet = models.ForeignKey(Fleet)
    character = models.ForeignKey(Character)
    from_ship = models.ForeignKey(Item, related_name="from_ship")
    to_ship = models.ForeignKey(Item, related_name="to_ship")
    timestamp = models.DateTimeField(auto_now_add=True)
