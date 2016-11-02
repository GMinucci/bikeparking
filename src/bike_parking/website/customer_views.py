# -*- coding: utf-8 -*-
from django.urls import reverse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, View
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.contrib import messages
from parking.models import ParkingLot, Location, Person, ParkingSpace, Rental, Payment
from forms import LocationForm, ParkingLotForm, ParkingSpaceForm, RentalDetailForm, PersonDetailForm, PaymentDetailForm
from django.http import HttpResponse
from parking.reports import rentals_per_parking_lot_each_month, customer_latest_transactions, parking_space_status


class CreateOrLoginView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'website/customer/account_redirect/create_or_login.html', {})


class CustomerOverviewView(View):

    def get(self, request, *args, **kwargs):
        view_parameters = {
            'latest_transactions': customer_latest_transactions(request.user, 20),
        }
        return render(request, 'website/customer/overview/index.html', view_parameters)


class LoginRedirectView(View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('usuario-resumo')
        if not request.user.groups.filter(name='admin').exists():
            try:
                person = Person.objects.get(user=request.user)
                if person.cpf is "":
                    return redirect('usuario-criar-conta')
                return redirect('usuario-resumo')
            except:
                return redirect('usuario-criar-conta')
        else:
            return redirect('sistema-index')


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


class CustomerRentalList(ListView):
    template_name = 'website/customer/overview/rentals.html'
    context_object_name = 'rentals'
    queryset = Rental.objects.none()

    def get(self, request, *args, **kwargs):
        self.queryset = Rental.objects.filter(lodger__user=request.user)
        return super(CustomerRentalList, self).get(request, *args, **kwargs)


class CustomerPaymentsList(ListView):
    template_name = 'website/customer/overview/payments.html'
    context_object_name = 'payments'
    queryset = Payment.objects.none()

    def get(self, request, *args, **kwargs):
        self.queryset = Payment.objects.filter(rental__lodger__user=request.user)
        return super(CustomerPaymentsList, self).get(request, *args, **kwargs)
