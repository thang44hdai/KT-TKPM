from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_screen, name='home'),
    path('customer/login/', views.login_screen, name='customer_login'),
]
