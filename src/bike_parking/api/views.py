from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, views
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from parking.models import ParkingLot, Person, Rental
from parking.service import get_nearby_queryset
from .serializers import ParkingLotListSerializer, ParkingLotDetailSerializer, ProfileSerializer, \
    RentalListSerializer, RentalDetailSerializer, RentSerializer


class ParkingLotViewSet(viewsets.ModelViewSet):
    queryset = ParkingLot.objects.none()
    serializer_class = ParkingLotListSerializer

    def list(self, request, *args, **kwargs):
        """
        List all nearby ParkingLot
        :param request:
            - lat: Latitude
            - lng: Longitude
        :return:
        """
        queryset = get_nearby_queryset(request.GET.get('lat', 0), request.GET.get('lng', 0)).filter(active=True)
        serializer = ParkingLotListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        Return details of one ParkingLot
        :param request:
        :param pk:
        :return:
        """
        queryset = get_object_or_404(ParkingLot, pk=pk)
        serializer = ParkingLotDetailSerializer(queryset, many=False)
        return Response(serializer.data)

    @detail_route(permission_classes=[IsAuthenticated],
                  authentication_classes=[SessionAuthentication, BasicAuthentication],
                  methods=['post'])
    def rent(self, request, pk):
        """
        * Requires authenticated user *
        Start a Rental for one ParkingSpace
        :param request:
        :param pk:
        :return:
        """
        data = dict(request.data.iteritems())
        data['lodger'] = get_object_or_404(Person, user=request.user).pk
        serializer = RentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class RentalsViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Rental.objects.none()
    serializer_class = RentalListSerializer

    def list(self, request):
        """
        * Requires authenticated user *
        List all Rental from one user
        :param request:
        :return:
        """
        queryset = Rental.objects.filter(lodger__user=request.user).exclude(rental_status='closed').order_by('start_time')
        serializer = RentalListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        * Requires authenticated user *
        Display details of one Rental
        :param request:
        :param pk:
        :return:
        """
        queryset = get_object_or_404(Rental, lodger__user=request.user, pk=pk)
        serializer = RentalDetailSerializer(queryset, many=False)
        return Response(serializer.data)

    @list_route(methods=['get'])
    def history(self, request):
        queryset = Rental.objects.filter(lodger__user=request.user, rental_status='closed').order_by('start_time')
        serializer = RentalListSerializer(queryset, many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def close(self, request, pk):
        rental = get_object_or_404(Rental, pk=pk, lodger__user=request.user)
        rental.end_time = timezone.now()
        rental.save()
        serializer = RentalDetailSerializer(rental, many=False)
        return Response(serializer.data)


class ProfileViewSet(views.APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        * Requires authenticated user *
        Display profile details of the current user
        :param request:
        :return:
        """
        queryset = get_object_or_404(Person, user=request.user)
        serializer = ProfileSerializer(queryset, many=False)
        return Response(serializer.data)
