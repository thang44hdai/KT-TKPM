from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

from book.models import Book
from clothes.models import Clothes
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
