from django.db import models
from django.core.cache import cache

from capritools2.models import *


class Fleet_Jump(models.Model):
    fleet = models.ForeignKey(Fleet, related_name="jumps")
    character = models.ForeignKey(Character)
    from_system = models.ForeignKey(System, related_name="from_system")
    to_system = models.ForeignKey(System, related_name="to_system")
    timestamp = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-timestamp']


    def export(self, character=False):
        key = "fleet_jump___%s_%s" % (self.id, character)
        out = cache.get(key)
        if out != None:
            return out

        out = {
            "from_system": self.from_system.export(),
            "to_system": self.to_system.export(),
            "timestamp": self.timestamp.isoformat()
        }
        if character:
            out['character'] = self.character.export()
            if out['character']['name'] != None:
                cache.set(key, out, 3600)
        else:
            cache.set(key, out, 3600)
        return out
