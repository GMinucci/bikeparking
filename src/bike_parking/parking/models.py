from __future__ import unicode_literals

import math

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from geopy.geocoders import GoogleV3

# Models Enum declarations
parking_space_status = (
    ('idle', 'Livre'),
    ('leased', 'Alugado'),
    ('occupied', 'Ocupado'),
    ('broken', 'Quebrado'),
)

bicycle_status = (
    ('idle', 'Livre'),
    ('leased', 'Alugado'),
    ('broken', 'Quebrado'),
)

rental_type = (
    ('space', 'Aluguel de vaga'),
    ('bicycle', 'Aluguel de bicicleta'),
)

rental_status = (
    ('open', 'Aberto'),
    ('closed', 'Fechado'),
    ('paid', 'Pago'),
)

payment_status = (
    ('open', 'Aberto'),
    ('confirmed', 'Confirmado'),
    ('refused', 'Cancelado'),
)

payment_type = (
    ('credit_card', 'Cartao de credito'),
    ('debit_card', 'Cartao de debito'),
    ('bank_slip', 'Transferencia bancaria'),
)


class Person(models.Model):
    user = models.OneToOneField(User, related_name='Person')
    active = models.BooleanField('Ativo', default=True)
    phone = models.CharField('Telefone', max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __unicode__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)


class Location(models.Model):
    cep = models.CharField('CEP', max_length=15)
    street = models.CharField('Endereco', max_length=100)
    number = models.IntegerField('Numero')
    neighborhood = models.CharField('Bairro', max_length=50)
    city = models.CharField('Cidade', max_length=100)
    state = models.CharField('Estado', max_length=100)
    country = models.CharField('Pais', max_length=100)
    complement = models.CharField('Complemento', max_length=100, blank=True, null=True)
    latitude = models.FloatField('Latitude', blank=True, null=True)
    longitude = models.FloatField('Longitude', blank=True, null=True)

    class Meta:
        verbose_name = 'Localizacao'
        verbose_name_plural = 'Localizacoes'

    def __unicode__(self):
        return "%s, %s" % (self.street, self.number)

    def save(self, *args, **kwargs):
        if not self.latitude or self.longitude:
            geolocator = GoogleV3()
            location = geolocator.geocode(', '.join([self.street, '%i' % self.number, self.neighborhood, self.city, self.state, self.country]))
            self.latitude = location.latitude
            self.longitude = location.longitude
        super(Location, self).save(*args, **kwargs)


class ParkingLot(models.Model):
    owner = models.ForeignKey(Person, related_name='parking_lots')
    location = models.ForeignKey(Location)
    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descricao', blank=True, null=True)
    default_price = models.FloatField('Preco padrao')
    per_hour_price = models.FloatField('Preco por hora')
    active = models.BooleanField('Ativo')

    class Meta:
        verbose_name = 'Estacionamento'
        verbose_name_plural = 'Estacionamentos'

    def __unicode__(self):
        return self.name


class ParkingSpace(models.Model):
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE, related_name='parking_spaces')
    number = models.IntegerField('Numero')
    status = models.CharField(choices=parking_space_status, max_length=20)

    class Meta:
        verbose_name = 'Vaga'
        verbose_name_plural = 'Vagas'

    def __unicode__(self):
        return "%i- %s - %s" % (self.number, self.get_status_display(), self.parking_lot)


class Bicycle(models.Model):
    parking_space = models.ForeignKey(ParkingSpace)
    status = models.CharField(choices=bicycle_status, max_length=20)
    model = models.CharField('Modelo', max_length=100)
    serial_number = models.CharField('Numero de serie', max_length=100)

    class Meta:
        verbose_name = 'Bicicleta'
        verbose_name_plural = 'Bicicletas'

    def __unicode__(self):
        return self.model


class Rental(models.Model):
    lodger = models.ForeignKey(Person, related_name='rentals')
    parking_space = models.ForeignKey(ParkingSpace, related_name='rentals')
    rental_type = models.CharField('Tipo de locacao', choices=rental_type, max_length=50)
    rental_status = models.CharField('Status da locacao', choices=rental_status, max_length=50, blank=True)
    start_time = models.DateField('Data de inicio', blank=True)
    end_time = models.DateField('Data de termino', blank=True, null=True)
    total = models.FloatField('Total', blank=True, null=True)

    class Meta:
        verbose_name = 'Aluguel'
        verbose_name_plural = 'Alugueis'

    def __unicode__(self):
        return "%s - %s, %s" % (self.get_rental_status_display(), self.start_time, self.end_time)

    def update_rental_status(self):
        if not self.start_time:
            self.start_time = timezone.now()
        if self.start_time and not self.end_time:
            self.rental_status = 'open'
        if self.start_time and self.end_time and self.rental_status == 'open':
            self.rental_status = 'closed'

    def update_rental_total_price(self):
        if self.rental_status == 'closed':
            # delta_time is the delta time in hours from start_time to end_time
            delta_time = (self.end_time - self.start_time).total_seconds() // 3600
            _, total_hours = math.modf(delta_time)
            self.total = self.parking_space.parking_lot.default_price
            self.total += total_hours * self.parking_space.parking_lot.per_hour_price

    def save(self, *args, **kwargs):
        self.update_rental_status()
        self.update_rental_total_price()
        super(Rental, self).save(*args, **kwargs)


class Payment(models.Model):
    rental = models.ForeignKey(Rental, related_name='payments')
    date = models.DateField('Data de pagamento')
    total = models.FloatField('Total', blank=True)
    payment_type = models.CharField(choices=payment_type, max_length=50)
    status = models.CharField(choices=payment_status, max_length=50, default='open')

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'

    def __unicode__(self):
        return "%f (%s) - %s" % (self.total, self.get_status_display(), self.date)

    def save(self, *args, **kwargs):
        if not self.total:
            self.total = self.rental.total
        super(Payment, self).save(*args, **kwargs)
