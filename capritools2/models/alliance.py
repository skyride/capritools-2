from django.db import models


class Alliance(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    ticker = models.CharField(max_length=5)
