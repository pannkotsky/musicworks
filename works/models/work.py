from django.contrib.postgres.fields import ArrayField, CICharField
from django.db import models
from django.utils.functional import cached_property

from works.managers import WorkManager
from .contributor import Contributor
from .source import Source


class Work(models.Model):
    iswc = models.CharField(max_length=11, null=True, blank=True, unique=True)
    source = models.ForeignKey(Source, on_delete=models.PROTECT, related_name='works')
    id_from_source = models.IntegerField()
    title = CICharField(max_length=256)
    title_synonyms = ArrayField(base_field=CICharField(max_length=256), blank=True,
                                default=list)
    contributors = models.ManyToManyField(Contributor, through='works.ContributorWork',
                                          related_name='works')

    objects = WorkManager()

    class Meta:
        unique_together = ('source', 'id_from_source',)

    def __str__(self):
        return f'{self.title} by {self.contributors_str}'

    @cached_property
    def contributors_str(self):
        return ', '.join(map(str, self.contributors.all()))

    def synonyms_str(self):
        return '|'.join(self.title_synonyms)

    def reconcile(self, data):
        """
        Find what information on the object can be added/updated from the new data
        about the object.

        Steps are the following:
        1. Assign iswc if it's not set on the object and present in the data.
        2. If title from the data is different from the current title, add it to title_synonyms.
        3. If there are new contributors in the data, add them to object relations.
        4. If something from above happened set source and id_from_source from the data and
           save the object.

        :param data: dict of prepared data for each field.
        :return: updated Work object.
        """

        from .contributor_work import ContributorWork

        changed = False

        if not self.iswc and data['iswc']:
            self.iswc = data['iswc']
            changed = True

        if self.title != data['title']:
            self.title_synonyms.append(data['title'])
            changed = True

        added_contributors = (set(data['contributors']) -
                              set(self.contributors.all()))
        for contributor in added_contributors:
            ContributorWork.objects.create(contributor=contributor, work=self)

        if self.source != data['source'] and (changed or added_contributors):
            self.source = data['source']
            self.id_from_source = data['id_from_source']
            changed = True

        if changed:
            self.save()

        return self
