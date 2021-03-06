# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-19 14:58
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bicycle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('idle', 'Livre'), ('leased', 'Alugado'), ('broken', 'Quebrado')], max_length=20)),
                ('model', models.CharField(max_length=100, verbose_name='Modelo')),
                ('serial_number', models.CharField(max_length=100, verbose_name='Numero de serie')),
            ],
            options={
                'verbose_name': 'Bicicleta',
                'verbose_name_plural': 'Bicicletas',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cep', models.CharField(max_length=15, verbose_name='CEP')),
                ('street', models.CharField(max_length=100, verbose_name='Endereco')),
                ('number', models.IntegerField(verbose_name='Numero')),
                ('neighborhood', models.CharField(max_length=50, verbose_name='Bairro')),
                ('city', models.CharField(max_length=100, verbose_name='Cidade')),
                ('state', models.CharField(max_length=100, verbose_name='Estado')),
                ('country', models.CharField(max_length=100, verbose_name='Pais')),
                ('complement', models.CharField(blank=True, max_length=100, null=True, verbose_name='Complemento')),
                ('latitude', models.FloatField(blank=True, null=True, verbose_name='Latitude')),
                ('longitude', models.FloatField(blank=True, null=True, verbose_name='Longitude')),
                ('point', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
            ],
            options={
                'verbose_name': 'Localizacao',
                'verbose_name_plural': 'Localizacoes',
            },
        ),
        migrations.CreateModel(
            name='ParkingLot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descricao')),
                ('default_price', models.DecimalField(decimal_places=2, max_digits=50, verbose_name='Preco padrao')),
                ('per_hour_price', models.DecimalField(decimal_places=2, max_digits=50, verbose_name='Preco por hora')),
                ('active', models.BooleanField(verbose_name='Ativo')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parking.Location')),
            ],
            options={
                'verbose_name': 'Estacionamento',
                'verbose_name_plural': 'Estacionamentos',
            },
        ),
        migrations.CreateModel(
            name='ParkingSpace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(blank=True, verbose_name='Numero')),
                ('status', models.CharField(choices=[('idle', 'Livre'), ('leased', 'Alugado'), ('occupied', 'Ocupado'), ('broken', 'Quebrado')], max_length=20)),
                ('bicycle', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parking_space', to='parking.Bicycle')),
                ('parking_lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parking_spaces', to='parking.ParkingLot')),
            ],
            options={
                'verbose_name': 'Vaga',
                'verbose_name_plural': 'Vagas',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, null=True, verbose_name='Data de pagamento')),
                ('total', models.DecimalField(blank=True, decimal_places=2, max_digits=50, verbose_name='Total')),
                ('payment_type', models.CharField(blank=True, choices=[('credit_card', 'Cartao de credito'), ('billet', 'Boleto'), ('online_debit', 'Debito online'), ('pagseguro_balance', 'Saldo PagSeguro'), ('oi_paggo', 'Oi Paggo'), ('account_deposit', 'Deposito em conta')], max_length=50, null=True)),
                ('status', models.CharField(choices=[('open', 'Aberto'), ('under_review', 'Em analise'), ('confirmed', 'Confirmado'), ('refused', 'Cancelado')], default='open', max_length=50)),
                ('status_code', models.PositiveIntegerField(blank=True, null=True)),
                ('code', models.CharField(blank=True, max_length=200, null=True)),
                ('redirect_url', models.URLField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Pagamento',
                'verbose_name_plural': 'Pagamentos',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('phone', models.CharField(blank=True, max_length=100, null=True, verbose_name='Telefone')),
                ('cpf', models.CharField(max_length=11, verbose_name='CPF')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Person', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
        ),
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rental_type', models.CharField(choices=[('space', 'Aluguel de vaga'), ('bicycle', 'Aluguel de bicicleta')], max_length=50, verbose_name='Tipo de locacao')),
                ('rental_status', models.CharField(blank=True, choices=[('open', 'Aberto'), ('closed', 'Fechado'), ('paid', 'Pago')], max_length=50, verbose_name='Status da locacao')),
                ('start_time', models.DateTimeField(blank=True, verbose_name='Data de inicio')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='Data de termino')),
                ('total', models.DecimalField(blank=True, decimal_places=2, max_digits=50, null=True, verbose_name='Total')),
                ('pin_code', models.CharField(blank=True, max_length=4, verbose_name='Codigo PIN')),
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
        migrations.AddField(
            model_name='parkinglot',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parking_lots', to='parking.Person'),
        ),
    ]
