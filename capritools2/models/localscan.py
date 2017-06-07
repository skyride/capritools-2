from django.db import models
from django.contrib.auth.models import User

from system import System


class LocalScan(models.Model):
    key = models.CharField(max_length=40, unique=True, db_index=True)
    added = models.DateTimeField(auto_now_add=True, db_index=True)
    system = models.ForeignKey(System, null=True, default=None)
    user = models.ForeignKey(User, null=True, default=None)
