import rest_framework_filters as filters

from works.models import Work


class WorkFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name='id_from_source')

    class Meta:
        model = Work
        fields = {
            'iswc': ['exact', 'in'],
            'source': ['exact'],
        }
