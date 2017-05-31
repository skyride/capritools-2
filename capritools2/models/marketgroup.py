from django.db import models


class MarketGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    parentGroup = models.ForeignKey("self", null=True)
    name = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    icon = models.IntegerField(null=True)
    hasTypes = models.NullBooleanField()
