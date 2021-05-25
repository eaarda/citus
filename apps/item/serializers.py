from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

from .models import Item, ItemNote


class ItemNoteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ItemNote
        fields = ('id', 'note')


class ItemSerializer(WritableNestedModelSerializer):
    notes = ItemNoteSerializer(many=True, allow_null=True)

    class Meta:
        model = Item
        fields = ('id', 'code', 'barcode', 'name', 'notes', 'sales_price')
        read_only_fields = ['item_type']