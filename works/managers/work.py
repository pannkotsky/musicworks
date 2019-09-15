from django.db.models import Q
from django.db.models.manager import Manager


class WorkManager(Manager):
    def match(self, data):
        """
        Try to match existing Work instance in the best way possible by the data.

        If iswc is in data, try to find the match using the following tries:
        1. Matching iswc.
        2. Matching by source and id from source among the items without iswc.
        3. Matching by title and contributor among the items without iswc.

        If iswc is not in data:
        1. Matching by source and id from source.
        2. Matching by title and contributor.

        :param data: dict of prepared data for each field.
        :return: matched Work instance or None if match is not found.
        """

        match_by_source = Q(source=data['source'], id_from_source=data['id_from_source'])
        match_by_title = Q(title=data['title']) | Q(title_synonyms__contains=[data['title']])
        match_by_title_and_contributor = match_by_title & Q(contributors__in=data['contributors'])
        if data['iswc']:
            match_queries = [
                Q(iswc=data['iswc']),
                Q(iswc=None) & match_by_source,
                Q(iswc=None) & match_by_title_and_contributor,
            ]
        else:
            match_queries = [
                match_by_source,
                match_by_title_and_contributor,
            ]
        for query in match_queries:
            try:
                return self.get(query)
            except self.model.DoesNotExist:
                continue
        return None
