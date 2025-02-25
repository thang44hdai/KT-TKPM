from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

from book.models import Book
from clothes.models import Clothes
from customer.models import Customer
from mobile.models import Mobile


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
