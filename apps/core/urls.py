from django.urls import path
from . import views  # Import views dari aplikasi core

urlpatterns = [
    path('', views.home, name='home'),  # URL untuk halaman Home
]
