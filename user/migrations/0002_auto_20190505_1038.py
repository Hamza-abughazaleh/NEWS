# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-05 07:38
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 5, 10, 38, 28, 870785)),
        ),
    ]
