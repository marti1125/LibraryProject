from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView, View
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from . import models
from . import form


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lendbooks'] = models.LendBook.objects.all()
        context['books_available'] = models.Book.objects.filter(status='D')
        return context


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
    fields = ['name', 'authors', 'status']
    success_url = reverse_lazy('book_index')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        name = form.cleaned_data['name']

        book = models.Book(name=name)
        book.save()

        #author_list = models.Author.objects.filter(pk__in=author)
        #print(author_list)
        for author in form.cleaned_data['authors']:
            book.authors.add(author)
        print(book.authors.all())
        return HttpResponseRedirect(self.get_success_url())


class BookUpdate(UpdateView):
    template_name = 'book/update.html'
    model = models.Book
    fields = ['name', 'authors', 'status']
    success_url = reverse_lazy('book_index')


class BookDelete(DeleteView):
    model = models.Book
    success_url = reverse_lazy('book_index')

    # return without confirmation template
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class UserIndex(TemplateView):
    template_name = 'user/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = models.LibraryUser.objects.all()
        return context


class UserCreate(CreateView):
    template_name = 'user/add.html'
    model = models.LibraryUser
    fields = '__all__'
    success_url = reverse_lazy('user_index')


class UserUpdate(UpdateView):
    template_name = 'user/update.html'
    model = models.LibraryUser
    fields = '__all__'
    success_url = reverse_lazy('user_index')


class UserDelete(DeleteView):
    model = models.LibraryUser
    success_url = reverse_lazy('user_index')

    # return without confirmation template
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class LendBookCreate(CreateView):
    template_name = 'lendbook/add.html'
    form_class = form.LendBookForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        self.object = form.save(commit=False)

        name = form.cleaned_data['book']
        models.Book.objects.filter(name=name).update(status='N')

        form.save()

        return HttpResponseRedirect(self.get_success_url())


class LendBookUpdate(UpdateView):
    template_name = 'lendbook/update.html'
    model = models.LendBook
    fields = ['status', 'return_date']
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        print(self.object.status)
        if self.object.status == 'D':
            models.Book.objects.filter(name=self.object.book.name).update(status='D')
        if self.object.status != 'D':
            models.Book.objects.filter(name=self.object.book.name).update(status='N')

        form.save()
        return HttpResponseRedirect(self.get_success_url())