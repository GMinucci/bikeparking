from django.contrib.gis.geos import Point
from parking.models import ParkingLot


def get_nearby_queryset(lat, lng, radius=5000):
    """
    Return the queryset value filtered using passed location
    WITH USE OF GEODJANGO AND POSTGIS
    https://docs.djangoproject.com/en/dev/ref/contrib/gis/db-api/#distance-queries

    lat     = Latitude
    lng     = Longitude
    radius  = Search query radiusin meters, default is 5 km
    """
    pnt = Point(float(lng), float(lat))
    return ParkingLot.objects.filter(location__point__distance_lte=(pnt, radius))