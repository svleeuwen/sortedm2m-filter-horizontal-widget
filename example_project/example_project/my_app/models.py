from __future__ import unicode_literals
from django.db import models
from sortedm2m.fields import SortedManyToManyField
from django.utils.encoding import python_2_unicode_compatible



@python_2_unicode_compatible
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Book(models.Model):
    name = models.CharField(max_length=100)
    authors = SortedManyToManyField(Author)

    def __str__(self):
        return self.name
