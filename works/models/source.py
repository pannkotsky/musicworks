from django.db import models


class Source(models.Model):
    identifier = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
        return self.identifier
