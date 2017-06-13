from django.db import models

from capritools2.models import *


class Fleet_ShipChange(models.Model):
    fleet = models.ForeignKey(Fleet)
    character = models.ForeignKey(Character)
    from_ship = models.ForeignKey(Item, related_name="from_ship")
    to_ship = models.ForeignKey(Item, related_name="to_ship")
    timestamp = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-timestamp']


    def export(self):
        return {
            "id": self.id,
            "character": self.character.export(),
            "from_ship": self.from_ship.export(),
            "to_ship": self.to_ship.export(),
            "timestamp": str(self.timestamp)
        }
