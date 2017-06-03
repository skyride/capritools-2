from django.db import models


class Character(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)
