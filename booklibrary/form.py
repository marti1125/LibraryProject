from django import forms
from . import models


class LendBookForm(forms.ModelForm):
    book = forms.ModelChoiceField(queryset=models.Book.objects.filter(status='D'))

    class Meta:
        model = models.LendBook
        fields = ['status', 'library_user', 'book', 'lend_date']

