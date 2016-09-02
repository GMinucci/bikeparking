from rest_framework import viewsets
from parking.models import ParkingLot
from .serializers import ParkingLotListSerializer, ParkingLotDetailSerializer


class ParkingLotViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ParkingLot.objects.all()
    serializer_class = ParkingLotListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ParkingLotDetailSerializer
        if self.action == 'list':
            return ParkingLotListSerializer


# class ParkingLotDetailViewSet(viewsets.ReadOnlyModelViewSet):
#     pass
