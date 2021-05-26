from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
import uuid
from django.utils.timezone import now

from django_multitenant.models import TenantModel
from django_multitenant.fields import TenantForeignKey, TenantOneToOneField
from django_multitenant.mixins import TenantManagerMixin, TenantModelMixin

from .managers import UserManager


class Company(TenantModel):
    tenant_id = "id"
    name = models.CharField(max_length=100)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='companies')
    endDate = models.DateTimeField(default=now)

    class Meta:
        db_table="companies"


class TenantUser(AbstractUser, TenantModelMixin):

    tenant_id = "company_id"
    company = models.ForeignKey(Company, related_name='users', on_delete=models.CASCADE, blank=True, null=True)

    id = models.UUIDField(primary_key = True, unique=True, default = uuid.uuid4, editable = False)
    username = None
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('name'), max_length=80, null=True)
    phone = models.CharField(max_length=15, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table="users"
        unique_together = ["id","company"]

    def __str__(self):
        return self.email


class TenantCompanyUsers(TenantModel):
    tenant_id = "company_id"

    company = models.ForeignKey(Company, related_name="company_users", on_delete=models.CASCADE)
    user = models.ForeignKey(TenantUser, related_name="company_users", on_delete=models.CASCADE) #TenantForeignKey?

    class Meta:
        unique_together = ["id","company"]
        db_table="company_users"