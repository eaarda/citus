from rest_framework import viewsets
from rest_framework import generics, status, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView 
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from django.contrib.auth import login, authenticate, logout

from .models import Company, TenantCompanyUsers
from .serializers import CompanySerializer, LoginSerializer, TokenSerializer, TenantCompanyUsersSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_queryset(self):
        users = TenantCompanyUsers.objects.filter(user_id=self.request.user)
        company=[]
        for i in users:
            company.extend(list(Company.objects.filter(id=i.company_id)))
        return company


class TenantCompanyUsersViewSet(viewsets.ModelViewSet):
    queryset = TenantCompanyUsers.objects.all()
    serializer_class = TenantCompanyUsersSerializer


class TokenViewSet(TokenObtainPairView):
    serializer_class = TokenSerializer
    permission_classes = [AllowAny]


class LoginViewSet(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']

            if user:
                login(request, user)

                company_list = TenantCompanyUsers.objects.filter(user_id=self.request.user)

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
                else:
                    return Response(data,status.HTTP_200_OK)
                    
        return Response(status = status.HTTP_400_BAD_REQUEST)


class LogoutViewSet(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request, format=None):
        logout(request)
        return Response(status=status.HTTP_200_OK)