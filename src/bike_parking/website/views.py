from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render
from parking.models import ParkingLot


class IndexPage(View):
    def get(self, request):
        template = 'website/index.html'
        return render(request, template)


class LoginPage(View):
    def get(self, request):
        template = 'website/login.html'
        return render(request, template)


class TestPage(View):
    def get(self, request):
        parkings = ParkingLot.objects.all()
        template = 'website/test.html'
        return render(request, template, {'parkings': parkings})
