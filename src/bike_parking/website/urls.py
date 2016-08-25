from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    url(r'^$', views.IndexPage.as_view(), name='index'),
    url(r'^test_admin/', login_required(views.TestAdminPage.as_view()), name='test_admin'),
    url(r'^test_client/', login_required(views.TestClientPage.as_view()), name='test_client'),
]
