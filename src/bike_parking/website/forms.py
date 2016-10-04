from django import forms
# from  django.core.exceptions import ValidationError
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
# from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from parking.models import Location, ParkingLot, ParkingSpace


class LocationForm(forms.ModelForm):

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
        )


class ParkingLotForm(forms.ModelForm):

    class Meta:
        model = ParkingLot
        fields = (
            # owner = models.ForeignKey(Person, related_name='parking_lots')
            # location = models.ForeignKey(Location)
            'name',
            'description',
            'default_price',
            'per_hour_price',
            'active',
        )


class ParkingSpaceForm(forms.ModelForm):

    class Meta:
        model = ParkingSpace
        fields = (
            'status',
        )
