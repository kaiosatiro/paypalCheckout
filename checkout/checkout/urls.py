from django.urls import path, include
from .views import *

urlpatterns = [
    path('', cart, name='cart'),
    path('cart', cart, name='cart'),
    path('createorder', createorder, name='createorder'),
    path('checkout', checkout, name='checkout'),
    path('confirmation', confirmation, name='confirmation')
]