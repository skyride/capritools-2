from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User

from social_django.models import UserSocialAuth
from capritools2.models import System

from capritools2.esi import ESI


class Fleet(models.Model):
    id = models.BigIntegerField(primary_key=True)
    key = models.CharField(max_length=7, db_index=True)
    user = models.ForeignKey(User)
    token = models.ForeignKey(UserSocialAuth)
    active = models.BooleanField(default=True, db_index=True)
    motd = models.TextField(null=True)
    voice_enabled = models.NullBooleanField()
    registered = models.NullBooleanField()
    free_move = models.NullBooleanField()
    added = models.DateTimeField(auto_now_add=True)


    def commander(self):
        try:
            return self.members.get(role="fleet_commander").export()
        except Exception:
            return None


    def main_system(self):
        try:
            return System.objects.filter(
                fleet_members__fleet=self
            ).annotate(
                members=Count('fleet_members')
            ).order_by(
                '-members'
            ).first()
        except Exception:
            return None


    def __unicode__(self):
        return "id=%s" % self.id
