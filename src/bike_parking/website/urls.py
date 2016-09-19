from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    url(r'^$', views.IndexPage.as_view(), name='index'),
    url(r'^admin/', login_required(views.AdminIndexPage.as_view()), name='admin_index'),
    url(r'^sistema/resumo/', login_required(views.SystemOverviewPage.as_view()), name='system_overview'),
    url(r'^sistema/estacionamentos/', login_required(views.SystemParkingLotIndexPage.as_view()),
        name='system_parkinglot'),
    url(r'^sistema/', login_required(views.SystemIndexPage.as_view()), name='system_index'),
]
