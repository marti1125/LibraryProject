# Generated by Django 3.1.7 on 2021-03-04 23:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booklibrary', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.CreateModel(
            name='Authored',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='booklibrary.author')),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='booklibrary.book')),
            ],
        ),
        migrations.AddField(
            model_name='author',
            name='books',
            field=models.ManyToManyField(through='booklibrary.Authored', to='booklibrary.Book'),
        ),
        migrations.AddField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(through='booklibrary.Authored', to='booklibrary.Author'),
        ),
    ]