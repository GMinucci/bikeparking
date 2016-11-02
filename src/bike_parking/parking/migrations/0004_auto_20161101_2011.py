# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-01 22:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0003_payment_last_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='owner',
            field=models.BooleanField(default=False, verbose_name='Proprietario'),
        ),
        migrations.AlterField(
            model_name='rental',
            name='parking_space',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rentals', to='parking.ParkingSpace', verbose_name='Vaga'),
        ),
    ]
