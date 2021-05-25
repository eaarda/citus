from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Company, TenantUser

from django.utils import timezone
import datetime


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
        company.save()

        user.name = validated_data['user_name']
        user.phone = validated_data['user_phone']
        user.company_id = self.company
        user.save()
        
        return company


class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super(LoginSerializer, self).validate(attrs)
        data.update(
            {"userData":
                {'email': self.user.email,
                }
            }
        )

        return data