from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, View
from django.shortcuts import render
from parking.models import ParkingLot


class IndexPage(View):
    template_name = 'website/index.html'


class LoginPage(TemplateView):
    template_name = 'website/login.html'


class TestAdminPage(ListView):
    template_name = 'website/test_admin.html'
    context_object_name = 'parkings'
    queryset = ParkingLot.objects.all()


class TestClientPage(ListView):
    template_name = 'website/test_client.html'
    context_object_name = 'parkings'
    queryset = ParkingLot.objects.all()

