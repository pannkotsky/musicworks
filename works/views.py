from rest_framework.settings import api_settings
from rest_framework_csv.renderers import CSVRenderer

from common.views import RetrieveOrCreateViewSet
from works.models import Contributor, Work
from .filters import WorkFilter
from .serializers import ContributorSerializer, WorkSerializer


class ContributorViewSet(RetrieveOrCreateViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    filterset_fields = ['verified']
    search_fields = ['first_name', 'last_name', 'middle_name']


class WorkViewSet(RetrieveOrCreateViewSet):
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
