from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'birth_date')