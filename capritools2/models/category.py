from django.db import models


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    icon = models.IntegerField(null=True)
    published = models.BooleanField()


    def __str__(self):
        return "id=%s name=%s" % (self.id, self.name)
