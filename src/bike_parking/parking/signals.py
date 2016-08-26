from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *


@receiver(post_save, sender=Rental)
def update_parking_space_status_from_rental(sender, **kwargs):
    rental = kwargs['instance']
    if rental.parking_space.status == 'broken':
        return
    if rental.end_time is None:
        rental.parking_space.status = 'leased'
    else:
        rental.parking_space.status = 'idle'
    rental.parking_space.save()


@receiver(post_save, sender=Bicycle)
def update_parking_space_from_bicycle(sender, **kwargs):
    bicycle = kwargs['instance']
    if bicycle.status == 'idle':
        bicycle.parking_space.status = 'occupied'
    if bicycle.status == 'leased':
        bicycle.parking_space.status = 'idle'
    bicycle.parking_space.save()
