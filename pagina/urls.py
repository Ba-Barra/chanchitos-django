from django.urls import path, include
from .views import index,productos,registrar,login,check_out,pedidos_usuario,carrito,dashboard

urlpatterns = [
    path('',index,name='base'),
    path('productos/',productos, name='productos'),
    path('registrar/',registrar,name='registrar'),
    path('login',login,name='login'),
    path('check_out',check_out,name='check_out'),
    path('pedidos_usuario',pedidos_usuario,name='pedidos_usuario'),
    path('carrito/',carrito, name='carrito'),
    path('dashboard/',dashboard,name='dashboard')
]
