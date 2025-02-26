from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response  # Import đúng từ DRF

from book.models import Book
from book.serializers import BookSerializer
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer  # Thêm JSONRenderer
from rest_framework import status
import datetime
from pymongo import MongoClient
from django.conf import settings
import json

# Create your views here.
client = MongoClient(settings.MONGO_URI)  # Lấy URI từ settings
db = client[settings.MONGO_DB_NAME]  # Database của bạn
collection = db["book"]  # Collection 'book'


def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})


class BookListAPI(APIView):
    renderer_classes = [JSONRenderer]  # Luôn trả về JSON

    def get(self, request, *args, **kwargs):
        books = Book.objects.using("mongodb").all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Thêm sách mới (sử dụng pymongo thay vì djongo)"""
        try:
            import json
            data = json.loads(request.body)

            # Chuẩn bị dữ liệu
            new_book = {
                "_id": data["_id"],  # Đảm bảo _id là unique
                "title": data["title"],
                "author": data["author"],
                "price": data["price"],
                "image": data["image"],
                "description": data["description"],
                "published_date": datetime.datetime.strptime(data["published_date"], "%Y-%m-%d")
            }

            # Chèn vào MongoDB bằng pymongo
            collection.insert_one(new_book)

            return JsonResponse({"message": "Book added successfully"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def put(self, request):
        try:
            data = json.loads(request.body)
            # Chuyển về string để phù hợp với CharField
            book_id = str(data.get("_id"))

            if not book_id:
                return JsonResponse({"error": "Missing book _id"}, status=400)

            update_data = {
                "title": data.get("title"),
                "author": data.get("author"),
                "price": data.get("price"),
                "image": data.get("image"),
                "description": data.get("description"),
                "published_date": datetime.datetime.strptime(data["published_date"], "%Y-%m-%d") if "published_date" in data else None
            }

            # Xóa các key có giá trị None
            update_data = {k: v for k, v in update_data.items()
                           if v is not None}

            # Cập nhật sách trong MongoDB
            result = collection.update_one(
                {"_id": book_id}, {"$set": update_data})

            if result.matched_count == 0:
                return JsonResponse({"error": "Book not found"}, status=404)

            return JsonResponse({"message": "Book updated successfully"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def delete(self, request):
        """Xóa sách bằng _id (dùng pymongo)"""
        try:
            data = json.loads(request.body)
            # Chuyển về string để phù hợp với CharField
            book_id = str(data.get("_id"))

            if not book_id:
                return JsonResponse({"error": "Missing book _id"}, status=400)

            # Xóa sách trong MongoDB
            result = collection.delete_one({"_id": book_id})

            if result.deleted_count == 0:
                return JsonResponse({"error": "Book not found"}, status=404)

            return JsonResponse({"message": "Book deleted successfully"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
