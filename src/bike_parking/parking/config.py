from django.apps import AppConfig
from django.db.models.signals import pre_save


class ParkingConfig(AppConfig):
    name = 'parking'

    def ready(self):
        from .signals import *
        pre_save.connect(receiver, sender='parking.Rental')
        pre_save.connect(receiver, sender='parking.Bicycle')
