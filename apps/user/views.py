from rest_framework import viewsets, generics, status, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView 
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from django.contrib.auth import login, authenticate, logout
from django_multitenant.utils import get_current_tenant, unset_current_tenant

from .models import Company, TenantCompanyUsers, TenantUser
from .serializers import CompanySerializer, LoginSerializer, TokenSerializer, TenantCompanyUsersSerializer, RegisterSerializer


class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_queryset(self):
        unset_current_tenant()
        user_companies = TenantCompanyUsers.objects.filter(user_id=self.request.user)
        company=[]
        for i in user_companies:
            company.extend(list(Company.objects.filter(id=i.company_id)))
        return company


class CompanyCreateViewSet(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CompanySerializer


class TenantCompanyUsersViewSet(viewsets.ModelViewSet):
    queryset = TenantCompanyUsers.objects.all()
    serializer_class = TenantCompanyUsersSerializer


class TokenViewSet(TokenObtainPairView):
    serializer_class = TokenSerializer
    permission_classes = [AllowAny]


class LoginViewSet(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"errors": serializer.errors},status.HTTP_400_BAD_REQUEST)
        
        email = serializer.data['email']
        password = serializer.data['password']

        if not TenantUser.objects.filter(email=email).exists():
            return Response({"message":"User does not exists."},status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email,password=password)

        if not user or user.is_anonymous:
            return Response({"message":"Email and password does not match."},status.HTTP_400_BAD_REQUEST)
        
        login(request,user)
        company_list = TenantCompanyUsers.objects.filter(user_id=user)

        data = {
            "user":user.id,
            "email":user.email,
            "company_count":len(company_list),
            "company_list":[]
        }
        if len(company_list)>0:
            for i in company_list:
                company = Company.objects.get(id=i.company_id)
                data['company_list'].append({
                                "company_id":i.company_id,
                                "company_name":company.name
                })
                
        return Response(data,status.HTTP_200_OK)


class RegisterViewSet(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class LogoutViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request, format=None):
        logout(request)
        return Response(status=status.HTTP_200_OK)