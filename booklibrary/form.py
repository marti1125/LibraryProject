from django.forms import ModelForm
from . import models


class AuthorForm(ModelForm):
    class Meta:
        model = models.Author
        fields = '__all__' #['first_name', 'last_name']

