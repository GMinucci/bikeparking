from rest_framework import viewsets
from parking.models import ParkingLot
from rest_framework.response import Response
from .serializers import ParkingLotListSerializer, ParkingLotDetailSerializer
from .service import get_nearby_queryset


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
        print request.GET
        print "COORDINATES %s %s" % (request.GET['lat'], request.GET['long'])
        queryset = get_nearby_queryset(request.GET['lat'], request.GET['long'])
        serializer = ParkingLotListSerializer(queryset, many=True)
        return Response(serializer.data)
        # print request.GET.get
