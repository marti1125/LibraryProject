from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    active = models.BooleanField(default=True)
    books = models.ManyToManyField('Book', through='Authored')

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Book(models.Model):
    name = models.CharField(max_length=100)
    authors = models.ManyToManyField('Author', through='Authored')

    def __str__(self):
        return "%s %s %s" % (self.name, self.author.first_name, self.author.last_name)


class Authored(models.Model):
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)


class LibraryUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)


class LendBook(models.Model):
    library_user = models.ForeignKey(LibraryUser, on_delete=models.SET_NULL, null=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    lend_date = models.DateField()

    def __str__(self):
        return "%s %s" % (self.library_user.name, self.book.name)