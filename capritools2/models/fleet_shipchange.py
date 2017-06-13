from django.db import models
from django.core.cache import cache

from capritools2.models import *


class Fleet_ShipChange(models.Model):
    fleet = models.ForeignKey(Fleet, related_name="ship_changes")
    character = models.ForeignKey(Character)
    from_ship = models.ForeignKey(Item, related_name="from_ship")
    to_ship = models.ForeignKey(Item, related_name="to_ship")
    timestamp = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-timestamp']


    def export(self, character=False):
        key = "fleet_ship_change_%s_%s" % (character, self.id)
        out = cache.get(key)
        if out != None:
            return out

        out =  {
            "id": self.id,
            "from_ship": self.from_ship.export(),
            "to_ship": self.to_ship.export(),
            "timestamp": str(self.timestamp)
        }
        if character:
            out['character'] = self.character.export()
            if out['character']['name'] != None:
                cache.set(key, out, 3600)
        else:
            cache.set(key, out, 3600)

        return out
