from django.shortcuts import render
from .models import Clothes

def clothes_list(request):
    clothes = Clothes.objects.all()
    return render(request, 'clothes_list.html', {'clothes_list': clothes})
