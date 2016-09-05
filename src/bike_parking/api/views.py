from rest_framework import viewsets
from parking.models import ParkingLot
from rest_framework.response import Response
from .serializers import ParkingLotListSerializer, ParkingLotDetailSerializer


class ParkingLotViewSet(viewsets.ModelViewSet):
    queryset = ParkingLot.objects.all()
    serializer_class = ParkingLotListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ParkingLotDetailSerializer
        if self.action == 'list':
            return ParkingLotListSerializer
        return ParkingLotListSerializer

    def list(self, request, *args, **kwargs):
        queryset = ParkingLot.objects.all()
        serializer = ParkingLotListSerializer(queryset, many=True)
        return Response(serializer.data)
        # print request.GET.get
