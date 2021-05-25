from rest_framework import viewsets

from apps.base.views import BaseModelViewSet, BaseReadOnlyModelViewSet
from .models import Item, ItemType
from .serializers import ItemSerializer


class ItemViewSet(BaseReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ProductViewSet(BaseModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_queryset(self):
        return self.queryset.filter(item_type=ItemType.PRODUCT)

    def perform_create(self, serializer):
        obj = serializer.save(item_type=ItemType.PRODUCT)
        obj.save()


class ServiceViewSet(BaseModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_queryset(self):
        return self.queryset.filter(item_type=ItemType.SERVICE)

    def perform_create(self, serializer):
        obj = serializer.save(item_type=ItemType.SERVICE)
        obj.save()