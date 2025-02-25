from django.shortcuts import render
from rest_framework.response import Response  # Import đúng từ DRF

from book.models import Book
from book.serializers import BookSerializer
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer  # Thêm JSONRenderer

# Create your views here.


def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})


class BookListAPI(APIView):
    renderer_classes = [JSONRenderer]  # Luôn trả về JSON

    def get(self, request, *args, **kwargs):
        books = Book.objects.using("mongodb").all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
