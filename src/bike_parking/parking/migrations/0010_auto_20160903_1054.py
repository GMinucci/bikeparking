# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-03 13:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0009_auto_20160902_1630'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bicycle',
            name='parking_space',
        ),
        migrations.AddField(
            model_name='parkingspace',
            name='bicycle',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parking_space', to='parking.Bicycle'),
        ),
    ]