from django.db import models
from sortedm2m.fields import SortedManyToManyField


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True)
    authors = SortedManyToManyField(Author)

    def __str__(self):
        return self.name
