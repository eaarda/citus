from django.urls import path, include
from rest_framework import routers

from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginViewSet, CompanyViewSet


router = routers.DefaultRouter()
router.register(r'companies', CompanyViewSet)


urlpatterns = [

    path('', include(router.urls)),

    path('token/', LoginViewSet.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]