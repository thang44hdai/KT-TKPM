from django.shortcuts import render
from .models import Mobile


def mobile_list(request):
    mobiles = Mobile.objects.all()  # Lấy tất cả dữ liệu từ MongoDB
    return render(request, 'mobile_list.html', {'mobiles': mobiles})
