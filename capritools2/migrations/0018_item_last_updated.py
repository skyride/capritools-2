# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-06 01:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capritools2', '0017_auto_20170606_0012'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='last_updated',
            field=models.DateTimeField(null=True),
        ),
    ]