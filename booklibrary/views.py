from django.shortcuts import render
from . import form


def author_view(request):
    author_form = form.AuthorForm()
    context = {'form': author_form}
    return render(request, 'book/author.html', context)
