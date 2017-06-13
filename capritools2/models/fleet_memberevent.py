from django.db import models

from capritools2.models import *


class Fleet_MemberEvent(models.Model):
    fleet = models.ForeignKey(Fleet, related_name="events")
    character = models.ForeignKey(Character)
    event = models.CharField(max_length=16, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-timestamp']


    def export(self):
        if self.event == "join":
            message = "%s joined fleet" % self.character.name
        if self.event == "leave":
            message = "%s left fleet" % self.character.name
        if self.event == "accept_fleetwarp":
            message = "%s flagged accept Fleet Warp" % self.character.name
        if self.event == "exempt_fleetwarp":
            message = "%s flagged exempt Fleet Warp" % self.character.name

        return {
            "id": self.id,
            "character": self.character.export(),
            "event": self.event,
            "message": message,
            "timestamp": str(self.timestamp)
        }
