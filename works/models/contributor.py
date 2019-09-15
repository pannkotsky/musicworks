from django.contrib.postgres.fields import CICharField
from django.db import models

from works.managers import ContributorManager


class Contributor(models.Model):
    first_name = CICharField(max_length=100, blank=True, default='', db_index=True)
    last_name = CICharField(max_length=100, db_index=True)
    middle_name = CICharField(max_length=100, blank=True, default='', db_index=True)
    # should be set to true when correctness of name parts is verified
    verified = models.BooleanField(default=False)

    objects = ContributorManager()

    def __str__(self):
        return self.full_name()

    def full_name(self):
        return ' '.join(filter(lambda x: x, (self.first_name, self.middle_name, self.last_name)))
