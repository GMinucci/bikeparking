from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render


class IndexPage(View):
    def get(self, request):
        template = 'website/index.html'
        return render(request, template)
