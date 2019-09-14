from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from works.models import Work
from .serializers import WorkSerializer


class WorkViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
