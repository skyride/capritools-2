from django.db import models
from django.contrib.auth.models import User

from social_django.models import UserSocialAuth

from capritools2.esi import ESI


class Fleet(models.Model):
    id = models.BigIntegerField(primary_key=True)
    key = models.CharField(max_length=7)
    user = models.ForeignKey(User)
    token = models.ForeignKey(UserSocialAuth)
    active = models.BooleanField(default=True, db_index=True)
    motd = models.TextField(null=True)
    voice_enabled = models.NullBooleanField()
    registered = models.NullBooleanField()
    free_move = models.NullBooleanField()


    def commander(self):
        try:
            return self.members.get(role="fleet_commander").export()
        except Exception:
            return None


    def __unicode__(self):
        return "id=%s" % self.id
