from parking.models import ParkingLot, Location, Person, ParkingSpace, Bicycle
from django.contrib.auth.models import User
from rest_framework import serializers


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = (
            'cep',
            'street',
            'number',
            'neighborhood',
            'city',
            'state',
            'country',
            'complement',
            'latitude',
            'longitude'
        )


class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )


class PersonDetailSerializer(serializers.HyperlinkedModelSerializer):
    user = UserDetailSerializer(many=False, read_only=True)

    class Meta:
        model = Person
        fields = (
            'phone',
            'user',
        )


class BicycleDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bicycle
        fields = (
            'status',
            'model',
            'serial_number'
        )


class ParkingSpaceListSerializer(serializers.HyperlinkedModelSerializer):
    # bicycle = BicycleDetailSerializer(many=False, read_only=True, allow_null=True)

    class Meta:
        model = ParkingSpace
        fields = (
            'id',
            'status',
            # 'bicycle',
        )


class ParkingLotListSerializer(serializers.HyperlinkedModelSerializer):
    location = LocationSerializer(many=False, read_only=True)

    class Meta:
        model = ParkingLot
        fields = (
            'id',
            # 'owner',
            'location',
            'name',
            'description',
            'default_price',
            'per_hour_price',
            'active',
        )


class ParkingLotDetailSerializer(serializers.HyperlinkedModelSerializer):
    location = LocationSerializer(many=False, read_only=True)
    owner = PersonDetailSerializer(many=False, read_only=True)
    parking_spaces = ParkingSpaceListSerializer(many=True, read_only=True)

    class Meta:
        model = ParkingLot
        fields = (
            'id',
            'owner',
            'location',
            'name',
            'description',
            'default_price',
            'per_hour_price',
            'active',
            'parking_spaces',
        )
