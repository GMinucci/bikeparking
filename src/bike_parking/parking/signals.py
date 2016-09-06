from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *


@receiver(post_save, sender=Rental)
def update_parking_space_status_from_rental(sender, **kwargs):
    """
    Called after save for Rental model to update ParkingSpace.status
    :param sender:
    :param kwargs:
    :return:
    """
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
    """
    Called after save on Bycicle model to update ParkingSpace.status
    :param sender:
    :param kwargs:
    :return:
    """
    bicycle = kwargs['instance']
    if bicycle.status == 'idle':
        bicycle.parking_space.status = 'occupied'
    if bicycle.status == 'leased':
        bicycle.parking_space.status = 'idle'
    bicycle.parking_space.save()


@receiver(post_save, sender=Payment)
def update_rental_status_from_payment(sender, **kwargs):
    """
    Called after save on Payment model to update Rental.rental_status
    :param sender:
    :param kwargs:
    :return:
    """
    payment = kwargs['instance']
    if payment.status == 'confirmed':
        payment.rental.rental_status = 'paid'
        payment.rental.save()
