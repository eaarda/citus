from django.contrib.auth import login, authenticate
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from django_multitenant.utils import set_current_tenant, unset_current_tenant
from django.utils import timezone
import datetime
from django.core.exceptions import ValidationError

from .models import Company, TenantUser, TenantCompanyUsers
from .tokens import RefreshToken


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

        try:
            user = TenantUser.objects.get(id=validated_data['createdBy'].id)
        
        except:
            raise serializers.ValidationError({"createdBy is not a valid UUID."})
            
        if user.company:
            raise serializers.ValidationError({"You can not create a new company."})

        else:
            company = Company.objects.create(name=validated_data['name'], createdBy=user)
            user.name = validated_data['user_name']
            user.phone = validated_data['user_phone']
            user.company = company
            user.save()
            TenantCompanyUsers.objects.create(company=company, user=user)
            set_current_tenant(company)
            
        return company



class TokenSerializer(TokenObtainSerializer):
    company = serializers.CharField()

    @classmethod
    def get_token(cls, user, company):
        return RefreshToken.for_user(user, company)
    
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user, attrs['company'])

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user'] = self.user.email
        data['company'] = attrs['company']

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
            data['user'] = user
        return data


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=TenantUser.objects.all())])
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True, validators=[validate_password])
    password1 = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)

    class Meta:
        model = TenantUser
        fields = ('id','email','password','password1')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password1']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self,validated_data):
        user = TenantUser.objects.create(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user