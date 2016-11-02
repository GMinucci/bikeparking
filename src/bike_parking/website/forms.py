from django import forms
# from  django.core.exceptions import ValidationError
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
# from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from parking.models import Location, ParkingLot, ParkingSpace, Rental, Payment


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
            'name',
            'description',
            'default_price',
            'per_hour_price',
            'active',
        )


class CustomerParkingLotForm(forms.ModelForm):

    class Meta:
        model = ParkingLot
        fields = (
            'name',
            'description',
            'default_price',
            'per_hour_price',
        )


class ParkingSpaceForm(forms.ModelForm):

    class Meta:
        model = ParkingSpace
        fields = (
            'status',
        )


class RentalDetailForm(forms.ModelForm):

    class Meta:
        model = Rental
        fields = (
            'parking_space',
            'rental_type',
            'rental_status',
            'start_time',
            'end_time',
            'total',
            'pin_code',
        )


class PaymentDetailForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = (
            'date',
            'total',
            'payment_type',
            'status',
            'redirect_url',
        )


class CustomerPaymentDetailForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = (
            'date',
            'total',
            'payment_type',
            'status',
        )


class PersonDetailForm(forms.Form):
    first_name = forms.CharField(label='Nome', max_length=100)
    last_name = forms.CharField(label='Sobrenome', max_length=100)
    email = forms.CharField(label='Email', max_length=100)
    phone = forms.CharField(label='Telefone', max_length=100)
    cpf = forms.CharField(label='CPF', max_length=11)
