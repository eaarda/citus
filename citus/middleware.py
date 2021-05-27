from django.core.exceptions import ValidationError
from rest_framework_simplejwt.backends import TokenBackend
from django.utils.deprecation import MiddlewareMixin
from django_multitenant.utils import (get_current_tenant, unset_current_tenant,
                                      get_tenant_column, set_current_tenant)

from apps.user.models import Company


class MultitenantMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        try:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            data = {'token': token}
            valid_data = TokenBackend(algorithm='HS256').decode(token,verify=False)
            company_id = valid_data['Company']
            company = Company.objects.get(id=company_id)
            unset_current_tenant()
            set_current_tenant(company)
            print("current tenant id:",get_current_tenant())
        
        except:
            pass

        return self.get_response(request)