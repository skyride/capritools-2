# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-12 18:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capritools2', '0035_auto_20170612_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fleet_squad',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='fleet_wing',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
    ]
