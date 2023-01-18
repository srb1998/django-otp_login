from .views import *
from django.urls import path,include
from . import views

urlpatterns = [
    path('cart',cart, name="cart")
]