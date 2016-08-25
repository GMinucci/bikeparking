from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from django.shortcuts import render
from parking.models import ParkingLot


class IndexPage(TemplateView):
    template_name = 'website/index.html'


class LoginPage(TemplateView):
    template_name = 'website/login.html'


class TestPage(ListView):
    template_name = 'website/test.html'
    context_object_name = 'parkings'
    queryset = ParkingLot.objects.all()
