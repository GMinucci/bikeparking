from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import IndexPage, SystemOverviewPage, SystemParkingLotInsertLocationFormView, \
    SystemParkingLotInsertUnity, SystemParkingLotIndexPage, SystemReportIndexPage, SystemAccountSettings, \
    SystemParkingLotDetailView, SystemParkingLotLocationEditView, \
    SystemParkingLotSpacesList, SystemParkingLotSpaceEditSpace, SystemReportPerUnity, SystemReportPerUnityRentals, \
    SystemReportPerUnityPayments, SystemReportRentals, SystemReportPayments, SystemReportRentalDetail, \
    SystemReportPaymentDetail
from .customer_views import CreateOrLoginView, CustomerOverviewView, CustomerAccountCreationView, CustomerRentalList, \
    CustomerPaymentsList, LoginRedirectView


urlpatterns = [
    url(r'^$',
        IndexPage.as_view(), name='index'),

    # url(r'^admin/',
    #     login_required(AdminIndexPage.as_view()), name='admin_index'),

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
    url(r'^sistema/relatorios/alugueis/(?P<rental_id>[0-9]+)/',
        login_required(SystemReportRentalDetail.as_view()), name='relatorios-alugueis-detalhe'),
    url(r'^sistema/relatorios/alugueis/',
        login_required(SystemReportRentals.as_view()), name='relatorios-alugueis'),
    url(r'^sistema/relatorios/pagamentos/(?P<payment_id>[0-9]+)/',
        login_required(SystemReportPaymentDetail.as_view()), name='relatorios-pagamentos-detalhe'),
    url(r'^sistema/relatorios/pagamentos/',
        login_required(SystemReportPayments.as_view()), name='relatorios-pagamentos'),
    url(r'^sistema/relatorios/',
        login_required(SystemReportIndexPage.as_view()), name='relatorios'),

    url(r'^sistema/configuracoes/',
        login_required(SystemAccountSettings.as_view()), name='configuracoes-conta'),

    url(r'^sistema/',
        login_required(SystemOverviewPage.as_view()), name='sistema-index'),

    url(r'^usuario/alugueis/',
        login_required(CustomerRentalList.as_view()), name='usuario-alugueis'),

    url(r'^usuario/pagamentos/',
        login_required(CustomerPaymentsList.as_view()), name='usuario-pagamentos'),

    url(r'^criar-ou-entrar/',
        CreateOrLoginView.as_view(), name='usuario-criar-ou-logar'),
    url(r'^usuario/criar-conta/',
        login_required(CustomerAccountCreationView.as_view()), name='usuario-criar-conta'),

    url(r'^usuario/',
        login_required(CustomerOverviewView.as_view()), name='usuario-resumo'),

    url(r'^login-redirect/',
        login_required(LoginRedirectView.as_view()), name='login-redirect'),
]
