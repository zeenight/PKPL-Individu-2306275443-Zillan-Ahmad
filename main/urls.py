from django.shortcuts import redirect
from django.urls import path
from main.views import show_register
from main.views import login_view
from main.views import logout_view
from main.views import home_view

app_name = 'main'

urlpatterns = [
    path('', lambda request: redirect('main:login_view')),  # Use namespaced redirect
    path('register/', show_register, name='show_register'),
    path('login/', login_view, name='login_view'),
    path("logout/", logout_view, name="logout"),
    path("home/", home_view, name="home"),
    
]