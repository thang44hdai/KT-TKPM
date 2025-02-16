from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

from book.models import Book


def home_screen(request):
    books = Book.objects.all()  # Lấy tất cả sách từ MongoDB
    return render(request, 'home.html', {'books': books})


def login_screen(request):
    template = loader.get_template('login.html')
    context = {}
    return HttpResponse(template.render(context, request))


def customer_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("")
        else:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng!")
    return render(request, "customer/login.html")
