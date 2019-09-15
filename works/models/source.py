from django.contrib.postgres.fields import CICharField
from django.db import models


class Source(models.Model):
    identifier = CICharField(max_length=30, primary_key=True)

    def __str__(self):
        return self.identifier
