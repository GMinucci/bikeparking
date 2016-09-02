from parking.models import ParkingLot, Location
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


class ParkingLotSerializer(serializers.HyperlinkedModelSerializer):
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
