from django.urls import path
from . import views

urlpatterns = [
    path('', views.clothes_list, name='clothes_list'),
]
