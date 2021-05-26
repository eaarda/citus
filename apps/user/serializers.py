from django.contrib.auth import login, authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django_multitenant.utils import set_current_tenant
from django.utils import timezone
import datetime

from .models import Company, TenantUser, TenantCompanyUsers


class TenantCompanyUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = TenantCompanyUsers
        fields = '__all__'
        

class CompanySerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(write_only=True)
    user_phone = serializers.CharField(write_only=True)

    class Meta:
        model = Company
        fields = ('id','name','user_name','user_phone','createdBy','endDate')
    
    def create(self,validated_data):
        user = self.context['request'].user
        user = TenantUser.objects.get(id=user.id)
        
        company = Company.objects.create(name=validated_data['name'], 
                                        createdBy=user)
        
        user.name = validated_data['user_name']
        user.phone = validated_data['user_phone']
        user.company = company
        user.save()

        compus = TenantCompanyUsers.objects.create(company_id=company.id, user_id=user.id)
        
        return company


class TokenSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super(TokenSerializer, self).validate(attrs)
        data.update(
            {"userData":
                {'email': self.user.email,
                }
            }
        )
        return data


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'},max_length=128,write_only=True)

    class Meta:
        model = TenantUser
        fields = ('email','password')
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(username=email, password=password)
            if user:
                data['user'] = user
            data['user'] = user
        return data