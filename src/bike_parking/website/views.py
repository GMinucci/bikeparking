from django.urls import reverse
from django.views.generic import TemplateView, ListView
from django.shortcuts import redirect
from parking.models import ParkingLot


class IndexPage(TemplateView):
    template_name = 'website/index.html'


class LoginPage(TemplateView):
    template_name = 'website/login.html'


class AdminIndexPage(ListView):
    template_name = 'website/admin/index.html'
    context_object_name = 'parkings'
    queryset = ParkingLot.objects.none()

    def get(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='admin').exists():
            return redirect(reverse('system_index'))
        self.queryset = ParkingLot.objects.filter(owner__user=request.user)
        return super(AdminIndexPage, self).get(request, *args, **kwargs)


class SystemIndexPage(ListView):
    template_name = 'website/system/index.html'
    context_object_name = 'parkings'
    queryset = ParkingLot.objects.filter(active=True)

    def get(self, request, *args, **kwargs):
        if request.user.groups.filter(name='admin').exists():
            return redirect(reverse('admin_index'))
        return super(SystemIndexPage, self).get(request, *args, **kwargs)
