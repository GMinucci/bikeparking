# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-05 19:08
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0010_auto_20160903_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
    ]