from django.apps import AppConfig
from django.db.models.signals import post_save
from django.dispatch import receiver


class ParkingConfig(AppConfig):
    name = 'parking'

    def ready(self):
        import signals
        post_save.connect(receiver, sender='parking.Rental')
        post_save.connect(receiver, sender='parking.Bicycle')
        post_save.connect(receiver, sender='parking.Payment')
