from django.urls import path, include
from .views import index,productos,registrar,login,check_out,pedidos_usuario,carrito,dashboard, chanchito , actualizarCarrito, cerrar_la_wea
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',index,name='index'),
    path('productos/',productos, name='productos'),
    path('accounts/register/',registrar,name='registrar'),
    path('accounts/login/',login,name='login'),
    path('check_out',check_out,name='check_out'),
    path('pedidos_usuario',pedidos_usuario,name='pedidos_usuario'),
    path('carrito/',carrito, name='carrito'),
    path('dashboard/',dashboard,name='dashboard'),
    path('dashboard/<uuid:id>', chanchito, name="detalle"),
    path('actualizar_chanchi_carrito/', actualizarCarrito),
    path('accounts/logout',cerrar_la_wea,name="logout")
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)