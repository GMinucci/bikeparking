# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-02 19:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0008_remove_parkingspace_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bicycle',
            name='parking_space',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bicycle', to='parking.ParkingSpace'),
        ),
    ]
