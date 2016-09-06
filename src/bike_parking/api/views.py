from django.shortcuts import get_object_or_404
from rest_framework import viewsets, views
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from parking.models import ParkingLot, Person, Rental
from rest_framework.response import Response
from .serializers import ParkingLotListSerializer, ParkingLotDetailSerializer, ProfileSerializer, RentalListSerializer
from .service import get_nearby_queryset


class ParkingLotViewSet(viewsets.ModelViewSet):
    queryset = ParkingLot.objects.none()
    serializer_class = ParkingLotListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ParkingLotDetailSerializer
        if self.action == 'list':
            return ParkingLotListSerializer
        return ParkingLotListSerializer

    def list(self, request, *args, **kwargs):
        queryset = get_nearby_queryset(request.GET.get('lat', 0), request.GET.get('lng', 0)).filter(active=True)
        serializer = ParkingLotListSerializer(queryset, many=True)
        return Response(serializer.data)


class RentalsViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.none()
    serializer_class = RentalListSerializer

    def list(self, request, *args, **kwargs):
        queryset = Rental.objects.filter(lodger__user=request.user)
        serializer = RentalListSerializer(queryset, many=True)
        return Response(serializer.data)


class ProfileViewSet(views.APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = get_object_or_404(Person, user=request.user)
        serializer = ProfileSerializer(queryset, many=False)
        return Response(serializer.data)
