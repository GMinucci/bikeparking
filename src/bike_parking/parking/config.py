from django.apps import AppConfig
from django.db.models.signals import post_save
from django.dispatch import receiver
from pagseguro.signals import notificacao_recebida


class ParkingConfig(AppConfig):
    name = 'parking'

    def ready(self):
        import signals
        from api.payment import pagseguro_load_signal
        post_save.connect(receiver, sender='parking.Rental')
        post_save.connect(receiver, sender='parking.Bicycle')
        post_save.connect(receiver, sender='parking.Payment')
        notificacao_recebida.connect(pagseguro_load_signal)
