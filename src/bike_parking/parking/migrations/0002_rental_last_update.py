# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-04 15:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rental',
            name='last_update',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Ultima atualizacao'),
            preserve_default=False,
        ),
    ]
