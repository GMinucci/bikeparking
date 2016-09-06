# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-26 17:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Data de pagamento')),
                ('total', models.FloatField(verbose_name='Total')),
                ('payment_type', models.CharField(choices=[('credit_card', 'Cartao de credito'), ('debit_card', 'Cartao de debito'), ('bank_slip', 'Transferencia bancaria')], max_length=50)),
                ('status', models.CharField(choices=[('open', 'Aberto'), ('confirmed', 'Confirmado'), ('refused', 'Cancelado')], max_length=50)),
            ],
            options={
                'verbose_name': 'Pagamento',
                'verbose_name_plural': 'Pagamentos',
            },
        ),
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rental_type', models.CharField(choices=[('space', 'Aluguel de vaga'), ('bicycle', 'Aluguel de bicicleta')], max_length=50)),
                ('rental_status', models.CharField(choices=[('open', 'Aberto'), ('closed', 'Fechado'), ('paid', 'Pago')], max_length=50)),
                ('start_time', models.DateField(verbose_name='Data de inicio')),
                ('end_time', models.DateField(blank=True, null=True, verbose_name='Data de termino')),
                ('lodger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rentals', to='parking.Person')),
                ('parking_space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rentals', to='parking.ParkingSpace')),
            ],
            options={
                'verbose_name': 'Aluguel',
                'verbose_name_plural': 'Alugueis',
            },
        ),
        migrations.AddField(
            model_name='payment',
            name='rental',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='parking.Rental'),
        ),
    ]