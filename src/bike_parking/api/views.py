from rest_framework import viewsets
from parking.models import ParkingLot
from .serializers import ParkingLotSerializer


class ParkingLotViewSet(viewsets.ModelViewSet):
    queryset = ParkingLot.objects.all()
    serializer_class = ParkingLotSerializer
