from django.db import models

from .contributor import Contributor
from .work import Work


class ContributorWork(models.Model):
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE,
                                    related_name='contributor_works')
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='contributor_works')

    class Meta:
        unique_together = ('contributor', 'work',)

    def __str__(self):
        return f'{self.work.title} by {self.contributor}'
