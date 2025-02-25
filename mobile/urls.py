from django.urls import path
from . import views

urlpatterns = [
    path('', views.mobile_list, name='mobile_list'),
]
