from django.conf.urls import url, include
from rest_framework import routers
from .views import ParkingLotViewSet, ProfileViewSet, RentalsViewSet


router = routers.DefaultRouter()
router.register(r'parkinglot', ParkingLotViewSet)
router.register(r'rentals', RentalsViewSet)

urlpatterns = [
    url(r'^profile/$', ProfileViewSet.as_view()),
    url(r'^', include(router.urls)),
    # url(r'^api-auth')
]