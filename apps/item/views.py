from rest_framework import viewsets

from apps.base.views import BaseModelViewSet, BaseReadOnlyModelViewSet
from apps.user.models import Company
from .models import Item, ItemType
from .serializers import ItemSerializer

from django_multitenant.utils import get_current_tenant


class ItemViewSet(BaseReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    
    def get_queryset(self):
        return self.queryset.filter(company_id=get_current_tenant())


class ProductViewSet(BaseModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_queryset(self):
        return self.queryset.filter(item_type=ItemType.PRODUCT,company_id=get_current_tenant())

    def perform_create(self, serializer):
        obj = serializer.save(item_type=ItemType.PRODUCT)
        obj.save()


class ServiceViewSet(BaseModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_queryset(self):
        return self.queryset.filter(item_type=ItemType.SERVICE, company_id=get_current_tenant())

    def perform_create(self, serializer):
        obj = serializer.save(item_type=ItemType.SERVICE)
        obj.save()