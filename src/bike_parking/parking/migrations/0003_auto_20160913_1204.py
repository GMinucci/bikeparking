# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-13 15:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0002_auto_20160912_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='code',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='redirect_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='status_code',
            field=models.PositiveIntegerField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=models.DateField(blank=True, null=True, verbose_name='Data de pagamento'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_type',
            field=models.CharField(blank=True, choices=[('credit_card', 'Cartao de credito'), ('debit_card', 'Cartao de debito'), ('bank_slip', 'Transferencia bancaria')], max_length=50, null=True),
        ),
    ]
