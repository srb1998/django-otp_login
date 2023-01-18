from django.contrib import admin
from django.urls import path,include
from . import views
from .views import *


urlpatterns = [
    path('', login, name ="login"),
    path('register', register, name="register"),
    path('otp', otp, name="otp"),
]