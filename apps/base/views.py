from rest_framework import viewsets, mixins, status, fields
from rest_framework.filters import SearchFilter, OrderingFilter
from url_filter.integrations.drf import DjangoFilterBackend


def _get_serializer_class(viewset):
    if viewset.list_serializer_class == None:
        viewset.list_serializer_class = viewset.serializer_class

    if viewset.action == 'list':
        return viewset.list_serializer_class
    return viewset.serializer_class


class BaseModelViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = '__all__'
    ordering_fields = '__all__'
    list_serializer_class = None

    class Meta:
        abstract = True

    def get_serializer_class(self):
        return _get_serializer_class(self)

class BaseReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = '__all__'
    ordering_fields = '__all__'
    list_serializer_class = None

    class Meta:
        abstract = True

    def get_serializer_class(self):
        return _get_serializer_class(self)