from django.db import models
from django.contrib.postgres.fields import ArrayField

from django_multitenant.fields import TenantForeignKey
from django_multitenant.models import TenantModel

from apps.user.models import Company


class ItemType(models.TextChoices):
    PRODUCT = 'product'
    SERVICE = 'service'


class Item(TenantModel):
    tenant_id = 'company_id'
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    item_type = models.CharField(max_length=20, choices=ItemType.choices, default=ItemType.PRODUCT)
    name = models.TextField()
    code = models.CharField(max_length=255, blank=True, null=True)
    barcode = models.CharField(max_length=255, blank=True, null=True)

    tracking = models.BooleanField(default=False)
    initial_quantity = models.FloatField(default=0.0)
    sales_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)

    class Meta(object):
        unique_together = ["id","company"]
        db_table = "items"

    def __str__(self):
        return self.name


class ItemNote(TenantModel):
    tenant_id = 'company_id'
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    item = TenantForeignKey(Item, on_delete=models.CASCADE,related_name="item_notes")

    note = models.TextField(blank=True, null=True)

    class Meta(object):
        unique_together = ["id","company"]
        db_table = "item_notes"

    def __str__(self):
        return self.note


class Catalog(TenantModel):
    tenant_id = 'company_id'
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    item = TenantForeignKey(Item, on_delete=models.CASCADE, related_name='catalogs')

    parent = models.ForeignKey('self', on_delete=models.PROTECT,related_name='children', null=True)
    barcode = models.CharField(max_length=50)
    title = models.TextField(null=True)

    class Meta(object):
        unique_together = ["id","company"]
        db_table = "catalogs"
    
    def __str__(self):
        return self.title