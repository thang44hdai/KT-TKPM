from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('api/books/', views.BookListAPI.as_view(), name='book-list'),
]
