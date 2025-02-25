from django.shortcuts import render

from book.models import Book

# Create your views here.


def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})
