from django.contrib.auth.models import User
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
        context['active_index'] = 'active'
        return context


class AuthorIndex(TemplateView):
    template_name = 'author/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = models.Author.objects.all()
        context['active_author'] = 'active'
        return context


class AuthorCreate(CreateView):
    template_name = 'author/add.html'
    form_class = form.AuthorForm
    # model = models.Author
    # fields = ['first_name', 'last_name', 'birth_date']
    success_url = reverse_lazy('author_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_author'] = 'active'
        return context


class AuthorUpdate(UpdateView):
    template_name = 'author/update.html'
    form_class = form.AuthorForm
    model = models.Author
    # fields = ['first_name', 'last_name', 'birth_date']
    success_url = reverse_lazy('author_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_author'] = 'active'
        return context


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
        context['active_book'] = 'active'
        return context


class BookCreate(CreateView):
    template_name = 'book/add.html'
    form_class = form.BookForm
    # model = models.Book
    # fields = ['name', 'authors', 'status']
    success_url = reverse_lazy('book_index')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        name = form.cleaned_data['name']

        book = models.Book(name=name)
        book.save()

        # author_list = models.Author.objects.filter(pk__in=author)
        # print(author_list)
        for author in form.cleaned_data['authors']:
            book.authors.add(author)
        print(book.authors.all())
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_book'] = 'active'
        return context


class BookUpdate(UpdateView):
    template_name = 'book/update.html'
    form_class = form.BookForm
    model = models.Book
    # fields = ['name', 'authors', 'status']
    success_url = reverse_lazy('book_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_book'] = 'active'
        return context


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
        print(models.LibraryUser.objects.all())
        context['active_user'] = 'active'
        return context


class UserCreate(CreateView):
    template_name = 'user/add.html'
    form_class = form.UserForm
    # model = models.LibraryUser
    # fields = '__all__'
    success_url = reverse_lazy('user_index')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        models.LibraryUser.objects.create(user=user)

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_user'] = 'active'
        return context


class UserUpdate(UpdateView):
    template_name = 'user/update.html'
    form_class = form.UserUpdateForm
    model = models.LibraryUser
    # fields = '__all__'
    success_url = reverse_lazy('user_index')

    def get_initial(self):
        library_user = models.LibraryUser.objects.get(id=self.get_object().pk)
        user = User.objects.get(id=library_user.user.id)
        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'username': user.username,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_user'] = 'active'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        library_user = models.LibraryUser.objects.get(id=self.get_object().pk)
        try:
            user = User.objects.get(id=library_user.user.id)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.username = form.cleaned_data['username']
            user.save()
        except:
            pass

        return HttpResponseRedirect(self.get_success_url())


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_index'] = 'active'
        return context


class LendBookUpdate(UpdateView):
    template_name = 'lendbook/update.html'
    form_class = form.LendBookUpdateForm
    model = models.LendBook
    # fields = ['status', 'return_date']
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_index'] = 'active'
        return context
