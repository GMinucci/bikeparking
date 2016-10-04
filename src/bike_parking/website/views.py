# -*- coding: utf-8 -*-
from django.urls import reverse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, View
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from parking.models import ParkingLot, Location, Person, ParkingSpace
from forms import LocationForm, ParkingLotForm
from django.http import HttpResponse


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


class SystemAccountSettings(TemplateView):
    template_name = 'website/system/account/settings.html'


class SystemOverviewPage(TemplateView):
    template_name = 'website/system/overview/index.html'


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

        if not location.is_valid():
            return HttpResponse(location.errors)
        else:
            return HttpResponse(parking_lot.errors)


class SystemParkingLotDetailView(View):

    def get(self, request, *args, **kwargs):
        parking_lot = get_object_or_404(ParkingLot, id=kwargs['pk'])
        last_transactions = parking_lot.get_last_transactions(5)
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
            return redirect('estacionamentos')
        return HttpResponse(parking_lot.errors)


class SystemParkingLotLocationEditView(View):

    def get(self, request, *args, **kwargs):
        parking_lot = get_object_or_404(ParkingLot, id=kwargs['pk'])
        return render(request, 'website/system/parking_lot/location-form.html',
                      {'form': LocationForm(instance=parking_lot.location)})

    def post(self, request, *args, **kwargs):
        parking_lot_instance = get_object_or_404(ParkingLot, id=kwargs['pk'])
        location = LocationForm(request.POST, instance=parking_lot_instance.location)
        if location.is_valid():
            location.save()
            return redirect('estacionamento-detalhe', kwargs['pk'])
        return HttpResponse(location.errors)


class SystemParkingLotSpacesList(ListView):
    template_name = 'website/system/parking_lot/parking_space_list.html'
    context_object_name = 'spaces'
    queryset = ParkingSpace.objects.none()

    def get(self, request, *args, **kwargs):
        self.queryset = ParkingSpace.objects.filter(parking_lot__id=kwargs['pk'])
        return super(SystemParkingLotSpacesList, self).get(request, *args, **kwargs)


class SystemReportIndexPage(TemplateView):
    template_name = 'website/system/report/index.html'


class SystemUserIndexPage(TemplateView):
    template_name = 'website/system/user/index.html'


