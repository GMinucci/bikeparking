from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as psmodels
from django.contrib.gis.geos import Point
from django.utils import timezone
from geopy.geocoders import GoogleV3
from .service import get_rental_total_price
import random

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
    ('under_review', 'Em analise'),
    ('confirmed', 'Confirmado'),
    ('refused', 'Cancelado'),
)

payment_type = (
    ('credit_card', 'Cartao de credito'),
    ('billet', 'Boleto'),
    ('online_debit', 'Debito online'),
    ('pagseguro_balance', 'Saldo PagSeguro'),
    ('oi_paggo', 'Oi Paggo'),
    ('account_deposit', 'Deposito em conta'),
)


class Person(models.Model):
    user = models.OneToOneField(User, related_name='Person')
    active = models.BooleanField('Ativo', default=True)
    phone = models.CharField('Telefone', max_length=100, blank=True, null=True)
    cpf = models.CharField('CPF', max_length=11)
    owner = models.BooleanField('Proprietario', blank=True, default=False)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __unicode__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    @classmethod
    def create(cls, person_data):
        user = User()
        user.username = person_data.get('email')
        user.email = person_data.get('email')
        user.first_name = person_data.get('first_name')
        user.last_name = person_data.get('last_name')
        user.set_password(person_data.get('password'))
        user.save()
        return cls(user=user, phone=person_data.get('phone'), cpf=person_data.get('cpf'))

    @classmethod
    def create_with_user(cls, user, person_data):
        user.first_name = person_data.get('first_name')
        user.last_name = person_data.get('last_name')
        user.save()
        return cls(user=user, phone=person_data.get('phone'), cpf=person_data.get('cpf'))


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
    point = psmodels.PointField(blank=True, null=True)

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
            self.point = Point(float(location.longitude), float(location.latitude))
        super(Location, self).save(*args, **kwargs)


class ParkingLot(models.Model):
    owner = models.ForeignKey(Person, related_name='parking_lots')
    location = models.ForeignKey(Location)
    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descricao', blank=True, null=True)
    default_price = models.DecimalField('Preco padrao', decimal_places=2, max_digits=50)
    per_hour_price = models.DecimalField('Preco por hora', decimal_places=2, max_digits=50)
    active = models.BooleanField('Ativo')

    class Meta:
        verbose_name = 'Estacionamento'
        verbose_name_plural = 'Estacionamentos'

    def __unicode__(self):
        return self.name

    def get_last_transactions(self, maxed):
        if maxed:
            return Rental.objects.filter(parking_space__parking_lot=self).order_by('-last_update')[:5]
        return Rental.objects.filter(parking_space__parking_lot=self).order_by('-last_update')

    def get_last_payments(self, maxed):
        if maxed:
            return Payment.objects.filter(rental__parking_space__parking_lot=self).order_by('-date')[:5]
        return Payment.objects.filter(rental__parking_space__parking_lot=self).order_by('-date')


class ParkingSpace(models.Model):
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE, related_name='parking_spaces')
    number = models.PositiveIntegerField('Numero', blank=True)
    status = models.CharField(choices=parking_space_status, max_length=20)
    bicycle = models.OneToOneField('Bicycle', related_name='parking_space', null=True, blank=True)

    class Meta:
        verbose_name = 'Vaga'
        verbose_name_plural = 'Vagas'

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = self.parking_lot.parking_spaces.count() + 1
        super(ParkingSpace, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%i" % self.number


class Bicycle(models.Model):
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
    parking_space = models.ForeignKey(ParkingSpace, verbose_name='Vaga', related_name='rentals')
    rental_type = models.CharField('Tipo de locacao', choices=rental_type, max_length=50)
    rental_status = models.CharField('Status da locacao', choices=rental_status, max_length=50, blank=True)
    start_time = models.DateTimeField('Data de inicio', blank=True)
    end_time = models.DateTimeField('Data de termino', blank=True, null=True)
    last_update = models.DateTimeField('Ultima atualizacao')
    total = models.DecimalField('Total', blank=True, null=True, decimal_places=2, max_digits=50)
    pin_code = models.CharField('Codigo PIN', blank=True, max_length=4)

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

    def create_pin_code(self):
        pin = random.randrange(1000, 9999)
        if self.parking_space.rentals.filter(pin_code=pin, rental_status='open').exists():
            return self.create_pin_code()
        return pin

    def save(self, *args, **kwargs):
        self.update_rental_status()
        if not self.total:
            self.total = get_rental_total_price(self)
        if not self.pin_code:
            self.pin_code = self.create_pin_code()
        self.last_update = timezone.now()
        super(Rental, self).save(*args, **kwargs)


class Payment(models.Model):
    rental = models.ForeignKey(Rental, related_name='payments')
    date = models.DateTimeField('Data de pagamento', blank=True, null=True)
    last_update = models.DateTimeField('Ultima atualizacao')
    total = models.DecimalField('Total', blank=True, decimal_places=2, max_digits=50)
    payment_type = models.CharField(choices=payment_type, max_length=50, blank=True, null=True)
    status = models.CharField(choices=payment_status, max_length=50, default='open')
    status_code = models.PositiveIntegerField(blank=True, null=True)
    code = models.CharField(max_length=200, blank=True, null=True)
    redirect_url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'

    def __unicode__(self):
        return "%s - %s" % (self.get_status_display(), self.date)

    def save(self, *args, **kwargs):
        if not self.total:
            self.total = self.rental.total
        self.last_update = timezone.now()
        super(Payment, self).save(*args, **kwargs)

    @classmethod
    def create(cls, rental):
        return cls(rental=rental, total=rental.total)
