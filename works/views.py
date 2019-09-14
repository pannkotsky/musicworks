from rest_framework import mixins
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet
from rest_framework_csv.renderers import CSVRenderer

from works.models import Work
from .filters import WorkFilter
from .serializers import WorkSerializer


class WorkViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES + [CSVRenderer]
    lookup_field = 'iswc'
    filterset_class = WorkFilter
    search_fields = ['title', 'contributors__first_name', 'contributors__last_name',
                     'contributors__middle_name']
    ordering_fields = ['title', 'iswc', 'source', 'id']

    def get_renderer_context(self):
        context = super().get_renderer_context()
        context['header'] = ['title', 'contributors', 'iswc', 'source', 'id']
        return context
