from django.urls import path, include
from rest_framework import routers

from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginViewSet, LogoutViewSet, TokenViewSet, CompanyViewSet, TenantCompanyUsersViewSet


router = routers.DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'test', TenantCompanyUsersViewSet)


urlpatterns = [

    path('', include(router.urls)),

    path('login/', LoginViewSet.as_view(), name="login"),
    path('logout/', LogoutViewSet.as_view(), name='logout'),

    path('token/', TokenViewSet.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]