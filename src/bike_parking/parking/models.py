from __future__ import unicode_literals
from django.db import models

# Models Enum declarations
parking_space_status = (
    ('idle', 'Livre'),
    ('leased', 'Alugado'),
    ('occupied', 'Ocupado'),
    ('broken', 'Quebrado'),
)


class Location(models.Model):
    cep = models.CharField('CEP', max_length=15)
    street = models.CharField('Endereco', max_length=100)
    number = models.IntegerField('Numero')
    neighborhood = models.CharField('Bairro', max_length=50)
    city = models.CharField('Cidade', max_length=100)
    complement = models.CharField('Complemento', max_length=100)
    latitude = models.FloatField('Latitude')
    longitude = models.FloatField('Longitude')


class ParkingLot(models.Model):
    location = models.ForeignKey(Location)
    description = models.TextField('Descricao')
    default_price = models.FloatField('Preco padrao')
    per_hour_price = models.FloatField('Preco por hora')
    active = models.BooleanField('Ativo')


class ParkingSpace(models.Model):
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE, related_name='parking_lot')
    status = models.CharField(choices=parking_space_status, max_length=20)


class Bicycle(models.Model):
    parking_space = models.ForeignKey(ParkingSpace)
    model = models.CharField('Modelo', max_length=100)
    serial_number = models.CharField('Numero de serie', max_length=100)



