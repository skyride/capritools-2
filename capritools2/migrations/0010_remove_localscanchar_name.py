# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-03 15:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('capritools2', '0009_auto_20170603_1531'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='localscanchar',
            name='name',
        ),
    ]
