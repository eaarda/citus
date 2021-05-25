from django.urls import path, include
from rest_framework import routers

from .views import ItemViewSet, ProductViewSet, ServiceViewSet


router = routers.DefaultRouter()
router.register(r"items", ItemViewSet)
router.register(r"products", ProductViewSet)
router.register(r"services", ServiceViewSet)


urlpatterns = [
    path('', include(router.urls)),
]