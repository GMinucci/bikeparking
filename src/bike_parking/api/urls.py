from django.conf.urls import url, include
from rest_framework import routers
from .views import ParkingLotViewSet, ProfileViewSet, RentalsViewSet, PaymentViewSet


router = routers.DefaultRouter()
router.register(r'parkinglot', ParkingLotViewSet)
router.register(r'rental', RentalsViewSet)
router.register(r'payment', PaymentViewSet)

urlpatterns = [
    url(r'^profile/$', ProfileViewSet.as_view()),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^', include(router.urls)),
]