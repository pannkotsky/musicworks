from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework_bulk.mixins import BulkCreateModelMixin


class RetrieveOrBulkCreateViewSet(BulkCreateModelMixin, mixins.RetrieveModelMixin,
                                  mixins.ListModelMixin, GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()` and `list()` actions.
    """
    pass
