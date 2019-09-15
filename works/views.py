from rest_framework.parsers import FormParser, JSONParser
from rest_framework.settings import api_settings
from rest_framework_csv.renderers import CSVRenderer

from common.parsers import CSVMultipartParser
from common.views import RetrieveOrBulkCreateViewSet
from works.models import Contributor, Source, Work
from .filters import WorkFilter
from .serializers import ContributorSerializer, SourceSerializer, WorkSerializer


class ContributorViewSet(RetrieveOrBulkCreateViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    filterset_fields = ['verified']
    search_fields = ['first_name', 'last_name', 'middle_name']


class SourceViewSet(RetrieveOrBulkCreateViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    search_fields = ['identifier']


class WorkViewSet(RetrieveOrBulkCreateViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    parser_classes = [JSONParser, FormParser, CSVMultipartParser]
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES + [CSVRenderer]
    lookup_field = 'iswc'
    filterset_class = WorkFilter
    search_fields = ['title', 'contributors__first_name', 'contributors__last_name',
                     'contributors__middle_name']
    ordering_fields = ['title', 'iswc', 'source', 'id']

    def get_renderer_context(self):
        context = super().get_renderer_context()
        context['header'] = ['title', 'synonyms', 'contributors', 'iswc', 'source', 'id']
        return context
