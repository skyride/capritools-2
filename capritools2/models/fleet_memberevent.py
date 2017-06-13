from django.db import models
from django.core.cache import cache

from capritools2.models import *


class Fleet_MemberEvent(models.Model):
    fleet = models.ForeignKey(Fleet, related_name="events")
    character = models.ForeignKey(Character)
    event = models.CharField(max_length=16, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-timestamp']


    def export(self, character=False):
        key = "Fleet_MemberEvent_%s_%s" % (character, self.id)
        out = cache.get(key)
        if out != None:
            return out

        if self.event == "join":
            message = "%s joined fleet" % self.character.name
        if self.event == "leave":
            message = "%s left fleet" % self.character.name
        if self.event == "accept_fleetwarp":
            message = "%s flagged accept Fleet Warp" % self.character.name
        if self.event == "exempt_fleetwarp":
            message = "%s flagged exempt Fleet Warp" % self.character.name

        out = {
            "id": self.id,
            "event": self.event,
            "message": message,
            "timestamp": str(self.timestamp)
        }
        if character:
            out['character'] = self.character.export()
            if out['character']['name'] != None:
                cache.set(key, out, 3600)
        else:
            cache.set(key, out, 3600)

        return out
