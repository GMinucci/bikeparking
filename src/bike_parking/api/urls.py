from django.conf.urls import url, include
from rest_framework import routers
from .views import ParkingLotViewSet


router = routers.DefaultRouter()
router.register(r'parkinglot', ParkingLotViewSet)
# router.register(r'parkinglot/(?P<pk>[0-9]+)/$', ParkingLotDetailViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^api-auth')
]