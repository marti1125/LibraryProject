from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime


# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Nombres')
    last_name = models.CharField(max_length=100, verbose_name='Apellidos')
    birth_date = models.DateField(verbose_name='Cumpleaños')
    active = models.BooleanField(default=True)
    books = models.ManyToManyField('Book', through='Authored')

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Book(models.Model):
    STATUS = (
        ('D', 'Disponible'),
        ('N', 'NoDisponible'),
    )
    name = models.CharField(max_length=100, verbose_name='Nombre')
    status = models.CharField(max_length=1, choices=STATUS, default='D', verbose_name='Estado')
    authors = models.ManyToManyField('Author', through='Authored', verbose_name='Autores')

    def __str__(self):
        return "%s" % self.name


class Authored(models.Model):
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)


class LibraryUser(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Nombres')
    last_name = models.CharField(max_length=100, verbose_name='Apellidos')
    birth_date = models.DateField(verbose_name='Cumpleaños')
    active = models.BooleanField(default=True)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


def validate_lend(value):
    count_days = value - datetime.now().date()
    print(count_days.days)
    if count_days.days < 0:
        raise ValidationError(
            ('Cantidad de dias invalido'),
            params={'value': value},
        )
    if count_days.days > 3:
        raise ValidationError(
            ('Solo se puede prestar como maximo 3 dias'),
            params={'value': value},
        )


class LendBook(models.Model):
    STATUS = (
        ('P', 'Prestado'),
        ('D', 'Devuelto'),
        ('N', 'NoDevuelto'),
    )
    status = models.CharField(max_length=1, choices=STATUS, default='D', verbose_name='Estado')
    library_user = models.ForeignKey(LibraryUser, on_delete=models.SET_NULL, null=True, verbose_name='Usuario')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, verbose_name='Libro')
    lend_date = models.DateField(validators=[validate_lend], verbose_name='Hasta que fecha')
    return_date = models.DateField(null=True, blank=True, verbose_name='Fecha de devolucion')

    def __str__(self):
        return "%s %s" % (self.library_user.name, self.book.name)

