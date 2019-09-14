from django.db import models
from django.utils.functional import cached_property

from .contributor import Contributor
from .source import Source


class Work(models.Model):
    iswc = models.CharField(max_length=11, blank=True, default='', unique=True)
    source = models.ForeignKey(Source, on_delete=models.PROTECT, related_name='works')
    id_from_source = models.IntegerField()
    title = models.CharField(max_length=256)
    contributors = models.ManyToManyField(Contributor, through='works.ContributorWork',
                                          related_name='works')

    class Meta:
        unique_together = ('source', 'id_from_source',)

    def __str__(self):
        return f'{self.title} by {self.contributors_str}'

    @cached_property
    def contributors_str(self):
        return ' | '.join(map(str, self.contributors.all()))
