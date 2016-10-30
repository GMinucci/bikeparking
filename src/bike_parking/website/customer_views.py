# -*- coding: utf-8 -*-
from django.urls import reverse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, View
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.contrib import messages
from parking.models import ParkingLot, Location, Person, ParkingSpace, Rental, Payment
from forms import LocationForm, ParkingLotForm, ParkingSpaceForm, RentalDetailForm, PersonDetailForm, PaymentDetailForm
from django.http import HttpResponse
from parking.reports import rentals_per_parking_lot_each_month, latest_transactions, parking_space_status


class CreateOrLoginView(TemplateView):
    template_name = 'website/customer/account_redirect/create_or_login.html'


class CustomerOverviewView(TemplateView):
    template_name = 'website/customer/account_redirect/create_or_login.html'


class CustomerAccountCreationView(View):

    def get(self, request, *args, **kwargs):
        person_form = PersonDetailForm(initial={
            'email': request.user.email,
        })
        return render(request, 'website/customer/account_redirect/account_creation.html', {
            'person_form': person_form,
        })

    def post(self, request, *args, **kwargs):
        person_form = PersonDetailForm(request.POST)
        if person_form.is_valid():
            person = Person.create_with_user(request.user, person_form.data)
            person.save()
            return redirect('usuario-resumo')
        return render(request, 'website/customer/account_redirect/account_creation.html', {
            'person_form': person_form,
        })
