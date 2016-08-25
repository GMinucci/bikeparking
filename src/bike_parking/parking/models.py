from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
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

    def save(self, *args, **kwargs):
        if self.status == 'idle':
            self.parking_space.status = 'occupied'
        if self.status == 'leased':
            self.parking_space.status = 'idle'
        self.parking_space.save()
        super(Bicycle, self).save(*args, **kwargs)


class Person(models.Model):
    user = models.OneToOneField(User, related_name='Person')
    active = models.BooleanField('Ativo', default=True)
    phone = models.CharField('Telefone', max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __unicode__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)
