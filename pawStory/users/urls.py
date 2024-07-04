# users/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('signup', signup_view, name='signup'),
    path('login', login_view, name='login'),
    path('pet_info', pet_info_view, name='pet_info'),
    path('check_user_id', check_user_id, name='check_user_id'),
]
