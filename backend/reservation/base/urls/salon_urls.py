from django.urls import include, path
from rest_framework import routers
from reservation.base.views import salon_views as views




router = routers.DefaultRouter()
router.register(r'salons', views.SalonViewSet)
router.register(r'courts', views.CourtViewSet)
router.register(r'reservations', views.ReservationViewSet)

urlpatterns = [
    # Other URLs in your project
    path('', include(router.urls)),
]
