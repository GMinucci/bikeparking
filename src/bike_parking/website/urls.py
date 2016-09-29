from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views
from django.views.generic.base import RedirectView


urlpatterns = [
    url(r'^$', views.IndexPage.as_view(), name='index'),
    url(r'^admin/', login_required(views.AdminIndexPage.as_view()), name='admin_index'),
    url(r'^sistema/resumo/', login_required(views.SystemOverviewPage.as_view()), name='resumo'),
    url(r'^sistema/estacionamentos/adicionar-unidade', login_required(views.SystemParkingLotInsertUnity.as_view()), name='adicionar-unidade'),
    url(r'^sistema/estacionamentos/', login_required(views.SystemParkingLotIndexPage.as_view()), name='estacionamentos'),
    url(r'^sistema/relatorios/', login_required(views.SystemReportIndexPage.as_view()), name='relatorios'),
    url(r'^sistema/usuarios/', login_required(views.SystemUserIndexPage.as_view()), name='usuarios'),
    url(r'^sistema/configuracoes/', login_required(views.SystemAccountSettings.as_view()), name='configuracoes-conta'),
    url(r'^sistema/', RedirectView.as_view(url='resumo/')),
]
