# -*- coding: utf-8 -*-
from django.urls import reverse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, View
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.contrib import messages
from parking.models import ParkingLot, Location, Person, ParkingSpace, Rental, Payment
from forms import LocationForm, ParkingLotForm, ParkingSpaceForm, RentalDetailForm, PersonDetailForm, PaymentDetailForm
from django.http import HttpResponse
from parking.reports import rentals_per_parking_lot_each_month, latest_transactions


class IndexPage(TemplateView):
    template_name = 'website/landing_page.html'


class LoginPage(TemplateView):
    template_name = 'website/login.html'


class AdminIndexPage(ListView):
    template_name = 'website/admin/index.html'
    context_object_name = 'parkings'
    queryset = ParkingLot.objects.none()

    def get(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='admin').exists():
            return redirect(reverse('resumo'))
        self.queryset = ParkingLot.objects.filter(owner__user=request.user)
        return super(AdminIndexPage, self).get(request, *args, **kwargs)


class SystemIndexPage(TemplateView):
    template_name = 'website/system/index.html'


class SystemAccountSettings(View):

    def get(self, request, *args, **kwargs):
        person = get_object_or_404(Person, user=request.user)
        person_form = PersonDetailForm(initial={
            'first_name': person.user.first_name,
            'last_name': person.user.last_name,
            'email': person.user.email,
            'phone': person.phone,
            'cpf': person.cpf
        })
        return render(request, 'website/system/settings/settings.html',{
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
        return render(request, 'website/system/settings/settings.html', {
            'person_form': person_form,
        })


class SystemOverviewPage(View):

    def get(self, request, *args, **kwargs):
        view_parameters = {
            'rental_month_report': rentals_per_parking_lot_each_month(request.user),
            'latest_transactions': latest_transactions(request.user, 20),
        }
        return render(request, 'website/system/overview/index.html', view_parameters)


class SystemOverviewRedirectPage(TemplateView):
    template_name = 'website/system/overview/index.html'

    def get(self, request, *args, **kwargs):
        return redirect(reverse('resumo'))


class SystemParkingLotIndexPage(ListView):
    template_name = 'website/system/parking_lot/index.html'
    context_object_name = 'parkinglots'
    queryset = ParkingLot.objects.none()

    def get(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='admin').exists():
            return redirect(reverse('resumo'))
        self.queryset = ParkingLot.objects.filter(owner__user=request.user)
        return super(SystemParkingLotIndexPage, self).get(request, *args, **kwargs)


class SystemParkingLotInsertLocationFormView(CreateView):
    model = Location
    template_name = 'website/system/parking_lot/location-form.html'
    form_class = LocationForm
    success_url = '/sistema/estacionamentos/'


class SystemParkingLotInsertUnity(View):

    def get(self, request, *args, **kwargs):
        forms = {
            u'Localização': LocationForm,
            u'Estacionamento': ParkingLotForm,
        }
        return render(request, 'website/system/parking_lot/new-parking-lot.html', {'forms': forms})

    def post(self, request, *args, **kwargs):
        location = LocationForm(request.POST)
        parking_lot = ParkingLotForm(request.POST)
        if location.is_valid() and parking_lot.is_valid():
            location_instance = location.save()
            parking_lot_instance = parking_lot.save(commit=False)
            parking_lot_instance.location = location_instance
            parking_lot_instance.owner = get_object_or_404(Person, user__id=request.user.id)
            parking_lot_instance.save()
            return redirect('estacionamentos')

        forms = {
            u'Localização': location,
            u'Estacionamento': parking_lot,
        }
        messages.add_message(request, messages.ERROR, 'Erro ao atualizar informações.')
        return render(request, 'website/system/parking_lot/new-parking-lot.html', {'forms': forms})


class SystemParkingLotDetailView(View):

    def get(self, request, *args, **kwargs):
        parking_lot = get_object_or_404(ParkingLot, id=kwargs['pk'])
        last_transactions = parking_lot.get_last_transactions(True)
        view_objects = {
            'parking_lot': parking_lot,
            'last_transactions': last_transactions,
            'form': ParkingLotForm(instance=parking_lot),
        }
        return render(request, 'website/system/parking_lot/detail.html', view_objects)

    def post(self, request, *args, **kwargs):
        instance = get_object_or_404(ParkingLot, id=kwargs['pk'])
        parking_lot = ParkingLotForm(request.POST, instance=instance)
        if parking_lot.is_valid():
            parking_lot.save()
            messages.add_message(request, messages.SUCCESS, 'Informações atualizadas com sucesso.')
            return redirect('estacionamentos')

        parking_lot_instance = get_object_or_404(ParkingLot, id=kwargs['pk'])
        last_transactions = parking_lot_instance.get_last_transactions(True)
        view_objects = {
            'parking_lot': parking_lot_instance,
            'last_transactions': last_transactions,
            'form': parking_lot,
        }
        messages.add_message(request, messages.ERROR, 'Erro ao atualizar informações.')
        return render(request, 'website/system/parking_lot/detail.html', view_objects)


class SystemParkingLotLocationEditView(View):

    def get(self, request, *args, **kwargs):
        parking_lot = get_object_or_404(ParkingLot, id=kwargs['pk'])
        return render(request, 'website/system/parking_lot/location-form.html', {
            'form': LocationForm(instance=parking_lot.location),
            'latitude': parking_lot.location.latitude,
            'longitude': parking_lot.location.longitude,
        })

    def post(self, request, *args, **kwargs):
        parking_lot_instance = get_object_or_404(ParkingLot, id=kwargs['pk'])
        location = LocationForm(request.POST, instance=parking_lot_instance.location)
        if location.is_valid():
            location.save()
            messages.add_message(request, messages.SUCCESS, 'Informações atualizadas com sucesso.')
            return redirect('estacionamento-detalhe', kwargs['pk'])
        messages.add_message(request, messages.ERROR, 'Erro ao atualizar informações.')
        return render(request, 'website/system/parking_lot/location-form.html',
                      {'form': location})


class SystemParkingLotSpacesList(ListView):
    template_name = 'website/system/parking_lot/parking_space_list.html'
    context_object_name = 'spaces'
    queryset = ParkingSpace.objects.none()

    def get(self, request, *args, **kwargs):
        self.queryset = ParkingSpace.objects.filter(parking_lot__id=kwargs['pk'])
        return super(SystemParkingLotSpacesList, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(SystemParkingLotSpacesList, self).get_context_data(*args, **kwargs)
        context['parking_lot'] = get_object_or_404(ParkingLot, id=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        parking_lot = get_object_or_404(ParkingLot, id=kwargs['pk'])
        ParkingSpace.objects.create(
            status='idle',
            parking_lot=parking_lot,
        )
        return redirect('estacionamento-detalhe-vagas', kwargs['pk'])


class SystemParkingLotSpaceEditSpace(View):

    def get(self, request, *args, **kwargs):
        parking_space = get_object_or_404(ParkingSpace, id=kwargs['space_pk'])
        return render(request, 'website/system/parking_lot/parking_space_form.html',
                      {'form': ParkingSpaceForm(instance=parking_space)})

    def post(self, request, *args, **kwargs):
        parking_space_instance = get_object_or_404(ParkingSpace, id=kwargs['space_pk'])
        parking_space = ParkingSpaceForm(request.POST, instance=parking_space_instance)
        if parking_space.is_valid():
            parking_space.save()
            messages.add_message(request, messages.SUCCESS, 'Informações atualizadas com sucesso.')
            return redirect('estacionamento-detalhe-vagas', kwargs['pk'])
        messages.add_message(request, messages.ERROR, 'Erro ao atualizar informações.')
        return render(request, 'website/system/parking_lot/parking_space_form.html',
                      {'form': parking_space})


class SystemReportIndexPage(TemplateView):
    template_name = 'website/system/report/index.html'


class SystemReportPerUnity(ListView):
    template_name = 'website/system/report/parking_space_report.html'
    context_object_name = 'parkinglots'
    queryset = ParkingLot.objects.none()

    def get(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='admin').exists():
            return redirect(reverse('resumo'))
        self.queryset = ParkingLot.objects.filter(owner__user=request.user)
        return super(SystemReportPerUnity, self).get(request, *args, **kwargs)


class SystemReportPerUnityRentals(ListView):
    template_name = 'website/system/report/parking_space_rental_report.html'
    context_object_name = 'rentals'
    queryset = Rental.objects.none()

    def get(self, request, *args, **kwargs):
        parking_lot = get_object_or_404(ParkingLot, id=kwargs['pk'])
        self.queryset = parking_lot.get_last_transactions(False)
        return super(SystemReportPerUnityRentals, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(SystemReportPerUnityRentals, self).get_context_data(**kwargs)
        context['parking_lot'] = get_object_or_404(ParkingLot, id=self.kwargs['pk'])
        return context


class SystemReportPerUnityPayments(ListView):
    template_name = 'website/system/report/parking_space_payment_report.html'
    context_object_name = 'payments'
    queryset = Payment.objects.none()

    def get(self, request, *args, **kwargs):
        parking_lot = get_object_or_404(ParkingLot, id=kwargs['pk'])
        self.queryset = parking_lot.get_last_payments(False)
        return super(SystemReportPerUnityPayments, self).get(request, *args, **kwargs)

    def get_context_data(self,*args ,**kwargs):
        context = super(SystemReportPerUnityPayments, self).get_context_data(**kwargs)
        context['parking_lot'] = get_object_or_404(ParkingLot, id=self.kwargs['pk'])
        return context


class SystemReportRentals(ListView):
    template_name = 'website/system/report/rentals.html'
    context_object_name = 'rentals'
    queryset = Rental.objects.none()

    def get(self, request, *args, **kwargs):
        self.queryset = Rental.objects.filter(parking_space__parking_lot__owner__user=request.user)
        return super(SystemReportRentals, self).get(request, *args, **kwargs)


class SystemReportRentalDetail(View):

    def get(self, request, *args, **kwargs):
        rental = get_object_or_404(Rental, id=kwargs['rental_id'])
        rental_form = RentalDetailForm(instance=rental)
        user_form = PersonDetailForm(initial={
                'first_name': rental.lodger.user.first_name,
                'last_name': rental.lodger.user.last_name,
                'email': rental.lodger.user.email,
                'active': rental.lodger.user.is_active,
                'phone': rental.lodger.phone,
                'cpf': rental.lodger.cpf
            })
        parking_lot_form = ParkingLotForm(instance=rental.parking_space.parking_lot)
        return render(request, 'website/system/report/detail/rental_detail.html',
                      {'rental_form': rental_form,
                       'user_form': user_form,
                       'parking_lot_form': parking_lot_form,
                       'rental_id': kwargs['rental_id']})


class SystemReportPayments(ListView):
    template_name = 'website/system/report/payments.html'
    context_object_name = 'payments'
    queryset = Payment.objects.none()

    def get(self, request, *args, **kwargs):
        self.queryset = Payment.objects.filter(rental__parking_space__parking_lot__owner__user=request.user)
        return super(SystemReportPayments, self).get(request, *args, **kwargs)


class SystemReportPaymentDetail(View):

    def get(self, request, *args, **kwargs):
        payment = get_object_or_404(Payment, id=kwargs['payment_id'])
        payment_form = PaymentDetailForm(instance=payment)
        user_form = PersonDetailForm(initial={
                'first_name': payment.rental.lodger.user.first_name,
                'last_name': payment.rental.lodger.user.last_name,
                'email': payment.rental.lodger.user.email,
                'active': payment.rental.lodger.user.is_active,
                'phone': payment.rental.lodger.phone,
                'cpf': payment.rental.lodger.cpf
            })
        rental_form = RentalDetailForm(instance=payment.rental)
        return render(request, 'website/system/report/detail/payment_detail.html',
                      {'payment_form': payment_form,
                       'user_form': user_form,
                       'rental_form': rental_form,
                       'payment_id': kwargs['payment_id']})
