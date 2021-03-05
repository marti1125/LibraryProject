from django.forms import ModelForm
from . import models


class AuthorForm(ModelForm):
    class Meta:
        model = models.Author
        fields = '__all__'


class BookForm(ModelForm):
    class Meta:
        model = models.Book
        fields = '__all__'

    def save(self, commit=True):
        author_book = super(AuthorForm, self).save(commit=False)
        author = self.cleaned_data['author']

        if commit:
            author_book.save()

        return author_book
