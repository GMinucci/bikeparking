from django.contrib.gis.geos import Point
import math


def get_nearby_queryset(lat, lng, radius=5000):
    """
    Return the queryset value filtered using passed location
    WITH USE OF GEODJANGO AND POSTGIS
    https://docs.djangoproject.com/en/dev/ref/contrib/gis/db-api/#distance-queries
    :param lat: Latitude
    :param lng: Longitude
    :param radius: Query radius in meters
    :return: Queryset
    """
    from .models import ParkingLot
    pnt = Point(float(lng), float(lat))
    return ParkingLot.objects.filter(location__point__distance_lte=(pnt, radius))


def get_rental_total_price(rental):
    """
    Return the total value of the rental passed if the rental_status is closed, using the formula:
    total = default_price + total_hours * per_hour_price
    :param rental: Rental object
    :return: total or None
    """
    if rental.rental_status == 'closed':
        delta_time = (rental.end_time - rental.start_time).total_seconds() // 3600
        _, total_hours = math.modf(delta_time)
        total = rental.parking_space.parking_lot.default_price
        total += total_hours * rental.parking_space.parking_lot.per_hour_price
        return total
    return None
