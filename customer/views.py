from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib import messages

from book.models import Book
from clothes.models import Clothes
from customer.models import Customer
from mobile.models import Mobile

from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Customer
from .serializers import RegisterSerializer, CustomerSerializer


def home_screen(request):
    books = Book.objects.all()[:6]  # Lấy 6 sách nổi bật
    mobiles = Mobile.objects.all()[:6]  # Lấy 6 điện thoại nổi bật
    clothes_list = Clothes.objects.all()[:6]  # Lấy 6 quần áo nổi bật
    return render(request, 'home.html', {
        'books': books,
        'mobiles': mobiles,
        'clothes_list': clothes_list
    })


def login_screen(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            # Tìm user trong bảng Customer
            customer = Customer.objects.get(username=username)

            # Kiểm tra mật khẩu (nếu lưu plain text)
            if password == customer.password:
                request.session["customer_id"] = customer.id  # Lưu vào session
                request.session["username"] = customer.username
                return redirect("home")
            else:
                messages.error(request, "Mật khẩu không đúng!")
        except Customer.DoesNotExist:
            messages.error(request, "Người dùng không tồn tại!")

    return render(request, "login.html")


def logout_screen(request):
    request.session.flush()  # Xóa session
    return redirect("home")


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Đăng ký thành công"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = Customer.objects.get(username=username)
            if password == user.password:  # So sánh trực tiếp với mật khẩu dạng string
                refresh = RefreshToken.for_user(user)
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                })
            return Response({"error": "Sai mật khẩu"}, status=status.HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
            return Response({"error": "Tài khoản không tồn tại"}, status=status.HTTP_400_BAD_REQUEST)


class CustomerView(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)
