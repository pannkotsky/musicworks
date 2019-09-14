from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class RetrieveOrCreateViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                              mixins.ListModelMixin, GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()` and `list()` actions.
    """
    pass
