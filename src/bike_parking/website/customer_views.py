# -*- coding: utf-8 -*-
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, View
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.contrib import messages
from parking.models import ParkingLot, Location, Person, ParkingSpace, Rental, Payment
from forms import LocationForm, ParkingLotForm, ParkingSpaceForm, RentalDetailForm, PersonDetailForm, PaymentDetailForm
from django.http import HttpResponse
from parking.reports import rentals_per_parking_lot_each_month, customer_latest_transactions, parking_space_status
from decorators import admin_redirect_on_user


@method_decorator(admin_redirect_on_user, name='dispatch')
class CreateOrLoginView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'website/customer/account_redirect/create_or_login.html', {})


@method_decorator(admin_redirect_on_user, name='dispatch')
class CustomerOverviewView(View):

    def get(self, request, *args, **kwargs):
        view_parameters = {
            'latest_transactions': customer_latest_transactions(request.user, 20),
        }
        return render(request, 'website/customer/overview/index.html', view_parameters)


class LoginRedirectView(View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('/account/login/')
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


@method_decorator(admin_redirect_on_user, name='dispatch')
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


@method_decorator(admin_redirect_on_user, name='dispatch')
class CustomerRentalList(ListView):
    template_name = 'website/customer/overview/rentals.html'
    context_object_name = 'rentals'
    queryset = Rental.objects.none()

    def get(self, request, *args, **kwargs):
        self.queryset = Rental.objects.filter(lodger__user=request.user)
        return super(CustomerRentalList, self).get(request, *args, **kwargs)


@method_decorator(admin_redirect_on_user, name='dispatch')
class CustomerPaymentsList(ListView):
    template_name = 'website/customer/overview/payments.html'
    context_object_name = 'payments'
    queryset = Payment.objects.none()

    def get(self, request, *args, **kwargs):
        self.queryset = Payment.objects.filter(rental__lodger__user=request.user)
        return super(CustomerPaymentsList, self).get(request, *args, **kwargs)


class CustomerAccountSettings(View):

    def get(self, request, *args, **kwargs):
        person = get_object_or_404(Person, user=request.user)
        person_form = PersonDetailForm(initial={
            'first_name': person.user.first_name,
            'last_name': person.user.last_name,
            'email': person.user.email,
            'phone': person.phone,
            'cpf': person.cpf
        })
        return render(request, 'website/customer/settings/index.html',{
            'person_form': person_form,
        })

    def post(self, request, *args, **kwargs):
        person_form = PersonDetailForm(request.POST)
        if person_form.is_valid():
            person = get_object_or_404(Person, user=request.user)
            person.__dict__.update(getattr(person_form, 'cleaned_data'))
            person.save()
            person.user.__dict__.update(getattr(person_form, 'cleaned_data'))
            person.user.save()
            messages.add_message(request, messages.SUCCESS, 'Informações atualizadas com sucesso.')
            return redirect('configuracoes-conta')
        messages.add_message(request, messages.ERROR, 'Erro ao atualizar informações.')
        return render(request, 'website/customer/settings/index.html', {
            'person_form': person_form,
        })
