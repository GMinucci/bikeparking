from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from parking.models import ParkingLot, Person, Rental, Payment
from parking.service import get_nearby_queryset
from .serializers import ParkingLotListSerializer, ParkingLotDetailSerializer, PersonDetailSerializer, \
    RentalListSerializer, RentalDetailSerializer, RentSerializer, RedirectPaymentSerializer, PaymentSerializer, \
    PaymentDetailSerializer, PersonCreatorSerializer
from payment import create_payment_attempt
from django.db.models import Q


class ParkingLotViewSet(viewsets.ViewSet):
    queryset = ParkingLot.objects.none()
    serializer_class = ParkingLotListSerializer

    def list(self, request, *args, **kwargs):
        """
        List all nearby ParkingLot
        ---

        serializer: api.serializers.ParkingLotListSerializer

        parameters:
            - name: lat
              description: Latitude
              required: false
              type: string
              paramType: form
            - name: lng
              description: Longitude
              required: false
              type: string
              paramType: form
        """
        queryset = get_nearby_queryset(request.GET.get('lat', 0), request.GET.get('lng', 0)).filter(active=True)
        serializer = ParkingLotListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        Return details of one ParkingLot
        ---

        serializer: api.serializers.ParkingLotDetailSerializer

        responseMessages:
            - code: 404
              message: Not found
        """
        queryset = get_object_or_404(ParkingLot, pk=pk)
        serializer = ParkingLotDetailSerializer(queryset, many=False)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def rent(self, request, pk):
        """
        Start a Rental for the first empty ParkingSpace using the user's cpf
        ---

        serializer: api.serializers.RentSerializer

        responseMessages:
            - code: 403
              message: Forbidden
            - code: 404
              message: Not found
        """
        data = dict(request.data.iteritems())
        data['lodger'] = get_object_or_404(Person, cpf=data.get('cpf')).pk
        serializer = RentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    @detail_route(methods=['post'])
    def close(self, request, pk):
        """
        Close one rental using PIN Code
        ---

        omit_parameters:
            - form

        responseMessages:
            - code: 404
              message: Not found
        """
        data = dict(request.data.iteritems())
        rental = get_object_or_404(Rental, pin_code=data.get('pin'))
        rental.end_time = timezone.now()
        rental.save()
        create_payment_attempt(rental)
        return JsonResponse({'status': 'OK'})


class RentalsViewSet(viewsets.ViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Rental.objects.none()
    serializer_class = RentalListSerializer
    http_method_names = ['get', 'post']

    def list(self, request):
        """
        **Requires authenticated user** \n
        Show open rental list information
        ---

        serializer: api.serializers.RentalListSerializer
        omit_parameters:
            - form

        responseMessages:
            - code: 403
              message: Forbidden
        """
        queryset = Rental.objects.filter(lodger__user=request.user, rental_status='open').order_by('start_time')
        serializer = RentalListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        **Requires authenticated user** \n
        Show rental detailed information
        ---

        serializer: api.serializers.RentalDetailSerializer
        omit_parameters:
            - form

        responseMessages:
            - code: 403
              message: Forbidden
        """
        queryset = get_object_or_404(Rental, lodger__user=request.user, pk=pk)
        serializer = RentalDetailSerializer(queryset, many=False)
        return Response(serializer.data)

    @list_route(methods=['get'])
    def history(self, request):
        """
        **Requires authenticated user** \n
        Show user closed and paid rental history list
        ---

        serializer: api.serializers.RentalListSerializer
        omit_parameters:
            - form

        responseMessages:
            - code: 403
              message: Forbidden
        """
        queryset = Rental.objects.filter(lodger__user=request.user).filter(~Q(rental_status='open')).\
            order_by('start_time')
        serializer = RentalListSerializer(queryset, many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def close(self, request, pk):
        """
        **Requires authenticated user** \n
        Close selected rental
        ---

        serializer: api.serializers.RentalDetailSerializer
        omit_parameters:
            - form

        responseMessages:
            - code: 403
              message: Forbidden
            - code: 404
              message: Not found
        """
        rental = get_object_or_404(Rental, pk=pk, lodger__user=request.user)
        rental.end_time = timezone.now()
        rental.save()
        serializer = RedirectPaymentSerializer(create_payment_attempt(rental), many=False)
        return Response(serializer.data)


class PaymentViewSet(viewsets.ViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Payment.objects.none()
    serializer_class = PaymentSerializer
    http_method_names = ['get']

    def list(self, request):
        """
        **Requires authenticated user** \n
        Show payment list information
        ---

        serializer: api.serializers.PaymentSerializer
        omit_parameters:
            - form

        responseMessages:
            - code: 403
              message: Forbidden
        """
        queryset = Payment.objects.filter(rental__lodger__user=request.user, status='open')
        serializer = PaymentSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        **Requires authenticated user** \n
        Show payment detailed information
        ---

        serializer: api.serializers.PaymentDetailSerializer
        omit_parameters:
            - form

        responseMessages:
            - code: 403
              message: Forbidden
        """
        queryset = get_object_or_404(Payment, rental__lodger__user=request.user, pk=pk)
        serializer = PaymentDetailSerializer(queryset, many=False)
        return Response(serializer.data)


class PersonViewSet(viewsets.ViewSet):
    queryset = Person.objects.none()
    serializer_class = PersonDetailSerializer
    http_method_names = ['get', 'post']

    @list_route(
        methods=['get'],
        permission_classes=[IsAuthenticated],
        authentication_classes=[SessionAuthentication, BasicAuthentication]
    )
    def profile(self, request):
        """
        **Requires authenticated user** \n
        Show current user profile
        ---

        serializer: api.serializers.ProfileSerializer

        responseMessages:
            - code: 403
              message: Forbidden
        """
        queryset = get_object_or_404(Person, user=request.user)
        serializer = PersonDetailSerializer(queryset, many=False)
        return Response(serializer.data)

    @list_route(methods=['post'])
    def new(self, request):
        """
        Create new user
        ---

        serializer: api.serializers.PersonCreatorSerializer

        responseMessages:
            - code: 403
              message: Forbidden
        """
        data = dict(request.data.iteritems())
        serializer = PersonCreatorSerializer(data=data)
        if serializer.is_valid():
            person = Person.create(serializer.data)
            person.save()
            return JsonResponse({'status': 'OK'})
        return Response(serializer.errors)



