from rest_framework import viewsets
from rest_framework import generics, status, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import login, authenticate, logout

from .models import Company, TenantCompanyUsers
from .serializers import CompanySerializer, LoginSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    #permissions_classes = [IsAuthenticated]

    def get_queryset(self):
        users = TenantCompanyUsers.objects.filter(user_id=self.request.user)
        company=[]
        for i in users:
            company.extend(list(Company.objects.filter(id=i.company_id)))
        return company


class LoginViewSet(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]