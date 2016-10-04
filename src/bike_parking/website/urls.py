from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .views import IndexPage, AdminIndexPage, SystemOverviewPage, SystemParkingLotInsertLocationFormView, \
    SystemParkingLotInsertUnity, SystemParkingLotIndexPage, SystemReportIndexPage, SystemUserIndexPage, \
    SystemAccountSettings, SystemOverviewRedirectPage, SystemParkingLotDetailView, SystemParkingLotLocationEditView, \
    SystemParkingLotSpacesList, SystemParkingLotSpaceEditSpace, SystemReportPerUnity, SystemReportPerUnityRentals, \
    SystemReportPerUnityPayments, SystemReportRentals
from django.views.generic.base import RedirectView


urlpatterns = [
    url(r'^$',
        IndexPage.as_view(), name='index'),

    url(r'^admin/',
        login_required(AdminIndexPage.as_view()), name='admin_index'),

    url(r'^sistema/resumo/',
        login_required(SystemOverviewPage.as_view()), name='resumo'),

    url(r'^sistema/adicionar-unidade/nova-localizacao/',
        login_required(SystemParkingLotInsertLocationFormView.as_view()), name='nova-localizacao'),
    url(r'^sistema/adicionar-unidade/',
        login_required(SystemParkingLotInsertUnity.as_view()), name='adicionar-unidade'),

    url(r'^sistema/estacionamentos/(?P<pk>[0-9]+)/vagas/(?P<space_pk>[0-9]+)/',
        login_required(SystemParkingLotSpaceEditSpace.as_view()), name='estacionamento-detalhe-vagas-editar'),
    url(r'^sistema/estacionamentos/(?P<pk>[0-9]+)/vagas/',
        login_required(SystemParkingLotSpacesList.as_view()), name='estacionamento-detalhe-vagas'),
    url(r'^sistema/estacionamentos/(?P<pk>[0-9]+)/editar-localizacao/',
        login_required(SystemParkingLotLocationEditView.as_view()), name='estacionamento-detalhe-localizacao'),
    url(r'^sistema/estacionamentos/(?P<pk>[0-9]+)/',
        login_required(SystemParkingLotDetailView.as_view()), name='estacionamento-detalhe'),
    url(r'^sistema/estacionamentos/',
        login_required(SystemParkingLotIndexPage.as_view()), name='estacionamentos'),

    url(r'^sistema/relatorios/unidades/(?P<pk>[0-9]+)/alugueis/',
        login_required(SystemReportPerUnityRentals.as_view()), name='relatorios-unidade-alugueis'),
    url(r'^sistema/relatorios/unidades/(?P<pk>[0-9]+)/pagamentos/',
        login_required(SystemReportPerUnityPayments.as_view()), name='relatorios-unidade-pagamentos'),
    url(r'^sistema/relatorios/unidades/',
        login_required(SystemReportPerUnity.as_view()), name='relatorios-por-unidade'),
    url(r'^sistema/relatorios/alugueis',
        login_required(SystemReportRentals.as_view()), name='relatorios-alugueis'),
    url(r'^sistema/relatorios/',
        login_required(SystemReportIndexPage.as_view()), name='relatorios'),

    url(r'^sistema/usuarios/',
        login_required(SystemUserIndexPage.as_view()), name='usuarios'),

    url(r'^sistema/configuracoes/',
        login_required(SystemAccountSettings.as_view()), name='configuracoes-conta'),

    url(r'^sistema/',
        login_required(SystemOverviewRedirectPage.as_view())),
]
