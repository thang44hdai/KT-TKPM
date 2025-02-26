from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_screen, name='home'),
    path('customer/login/', views.login_screen, name='customer_login'),
    path("customer/logout/", views.logout_screen, name="customer_logout"),
    path('api/register/', views.RegisterView.as_view(), name='register'),
    path('api/login/', views.LoginView.as_view(), name='login'),
    path('api/get-customers/', views.CustomerView.as_view(), name='customers'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
