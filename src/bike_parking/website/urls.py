from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    url(r'^$', views.IndexPage.as_view(), name='index'),
    url(r'^login/', views.LoginPage.as_view(), name='login'),
    url(r'^test/', login_required(views.TestPage.as_view()), name='test'),
]