from django.db import models
from django.contrib.auth.models import User


class Paste(models.Model):
    key = models.CharField(max_length=40, unique=True, db_index=True)
    added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, default=None)
    text = models.TextField()
    expires = models.DateTimeField(null=True)
    salt = models.CharField(max_length=32, null=True)
    password = models.CharField(max_length=64, null=True)
