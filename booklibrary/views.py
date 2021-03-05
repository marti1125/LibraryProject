from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView, View
from django.views.generic.base import TemplateView
from django.urls import reverse, reverse_lazy
from . import models
from . import form


class IndexView(TemplateView):
    template_name = 'index.html'


class AuthorIndex(TemplateView):
    template_name = 'author/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = models.Author.objects.all()
        return context


class AuthorCreate(CreateView):
    template_name = 'author/add.html'
    model = models.Author
    fields = ['first_name', 'last_name', 'birth_date']
    success_url = reverse_lazy('author_index')


class AuthorUpdate(UpdateView):
    template_name = 'author/update.html'
    model = models.Author
    fields = ['first_name', 'last_name', 'birth_date']
    success_url = reverse_lazy('author_index')


class AuthorDelete(DeleteView):
    model = models.Author
    success_url = reverse_lazy('author_index')

    # return without confirmation template
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class BookIndex(TemplateView):
    template_name = 'book/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = models.Book.objects.all()
        return context


class BookCreate(CreateView):
    template_name = 'book/add.html'
    model = models.Book
    fields = ['name', 'authors']
    success_url = reverse_lazy('book_index')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        name = form.cleaned_data['name']
        #author = form.cleaned_data['authors']

        book = models.Book(name=name)
        book.save()

        #author_list = models.Author.objects.filter(pk__in=author)
        #print(author_list)
        for author in form.cleaned_data['authors']:
            ##print(author)
            book.authors.add(author)
            ##print(book.authors.all())
        print(book.authors.all())
        #self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class BookUpdate(UpdateView):
    template_name = 'book/update.html'
    model = models.Book
    fields = ['name', 'authors']
    success_url = reverse_lazy('book_index')


class BookDelete(DeleteView):
    model = models.Book
    success_url = reverse_lazy('book_index')

    # return without confirmation template
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

