# Generated by Django 3.1.7 on 2021-03-06 21:37

import booklibrary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='Nombres')),
                ('last_name', models.CharField(max_length=100, verbose_name='Apellidos')),
                ('birth_date', models.DateField(verbose_name='Cumpleaños')),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Authored',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='booklibrary.author')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('status', models.CharField(choices=[('D', 'Disponible'), ('N', 'NoDisponible')], default='D', max_length=1, verbose_name='Estado')),
                ('authors', models.ManyToManyField(through='booklibrary.Authored', to='booklibrary.Author', verbose_name='Autores')),
            ],
        ),
        migrations.CreateModel(
            name='LibraryUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LendBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('P', 'Prestado'), ('D', 'Devuelto'), ('N', 'NoDevuelto')], default='D', max_length=1, verbose_name='Estado')),
                ('lend_date', models.DateField(validators=[booklibrary.models.validate_lend], verbose_name='Hasta que fecha')),
                ('return_date', models.DateField(blank=True, null=True, verbose_name='Fecha de devolucion')),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='booklibrary.book', verbose_name='Libro')),
                ('library_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='booklibrary.libraryuser', verbose_name='Usuario')),
            ],
        ),
        migrations.AddField(
            model_name='authored',
            name='book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='booklibrary.book'),
        ),
        migrations.AddField(
            model_name='author',
            name='books',
            field=models.ManyToManyField(through='booklibrary.Authored', to='booklibrary.Book'),
        ),
    ]
