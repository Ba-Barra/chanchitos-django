from django.urls import path, include
from .views import index,productos,registrar,login,check_out,pedidos_usuario,carrito,dashboard, chanchito , actualizarCarrito, cerrar_la_wea, pedidos_admin, detalle_boleta, editarProducto,eliminarProducto, misProductos,productos_usuario, editarEnvio, usuarios, editarUsuario,eliminarUsuario
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',index,name='index'),
    path('productos/',productos, name='productos'),
    path('accounts/register/',registrar,name='registrar'),
    path('accounts/login/',login,name='login'),
    path('check_out/',check_out,name='check_out'),
    path('pedidos_usuario',pedidos_usuario,name='pedidos_usuario'),
    path('carrito/',carrito, name='carrito'),
    path('dashboard/',dashboard,name='dashboard'),
    path('actualizar_chanchi_carrito/', actualizarCarrito),
    path('accounts/logout',cerrar_la_wea,name="logout"),
    path('dashboard/pedidos_admin', pedidos_admin, name="pedidos_admin"),
    path('dashboard/pedidos/<uuid:id>',detalle_boleta, name="detalle_boleta"),
    path('dashboard/producto/<uuid:id>',editarProducto,name="editar"),
    path('dashboard/producto/eliminar/<uuid:id>',eliminarProducto,name="eliminar"),
    path('mis_compras/',misProductos,name="misProductos"),
    path('mis_compras/<uuid:id>',productos_usuario,name="productos_usuario"),
    path('api/order/', editarEnvio),
    path('dashboard/usuarios',usuarios,name="usuarios"),
    path('dashboard/editarUsuario/<id>',editarUsuario,name="editarUsuario"),
    path('dashboard/eliminarUsuario/<id>',eliminarUsuario,name="eliminarUsuario")
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)