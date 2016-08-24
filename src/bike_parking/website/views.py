from django.http import HttpResponse
from django.views.generic.base import TemplateView


class IndexPage(TemplateView):
    template_name = 'templates/index.html'
