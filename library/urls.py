"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from booklibrary import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index'),
    path('authors', views.AuthorIndex.as_view(), name='author_index'),
    path('authors/add', views.AuthorCreate.as_view(), name='author_create'),
    path('authors/<int:pk>', views.AuthorUpdate.as_view(), name='author_update'),
    path('authors/<int:pk>/delete', views.AuthorDelete.as_view(), name='author_delete'),
    path('books', views.BookIndex.as_view(), name='book_index'),
    path('books/add', views.BookCreate.as_view(), name='book_create'),
    path('books/<int:pk>', views.BookUpdate.as_view(), name='book_update'),
    path('books/<int:pk>/delete', views.BookDelete.as_view(), name='book_delete'),
    path('users', views.UserIndex.as_view(), name='user_index'),
    path('users/add', views.UserCreate.as_view(), name='user_create'),
    path('users/<int:pk>', views.UserUpdate.as_view(), name='user_update'),
    path('users/<int:pk>/delete', views.UserDelete.as_view(), name='user_delete'),
    path('lendbooks', views.LendBookCreate.as_view(), name='lendbook_create'),
    path('lendbooks/<int:pk>', views.LendBookUpdate.as_view(), name='lendbook_update'),
]
