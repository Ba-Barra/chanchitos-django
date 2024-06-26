from django.shortcuts import render
from .models import Producto, Boleta, Detalle_boleta
from django.views.decorators.http import require_POST
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render (request,"core/index.html")

def productos(request):
    productos = Producto.objects.all()

    context = {'productos': productos}
    return render(request, "core/productos.html", context)

def registrar(request):
    return render(request, "core/registrar.html")

def login(request):
    return render(request,"core/login.html")

def check_out(request):
    return render(request,"core/check_out.html")

def pedidos_usuario(request):
    return render(request,"core/pedidos_usuario.html")


def carrito(request):
    if request.user.is_authenticated: 
        order,creada = Boleta.objects.get_or_create(cliente=request.user,completada=False)
        items = order.detalle_boleta_set.all()
        items_carrito = order.get_item
    else: 
        items = []
        order = {'get_total': 0,
                 'get_item': 0}
        items_carrito = order['get_item']
    context = {'items': items, 'order' : order}      
    

    return render(request, "core/carrito.html",context)

def dashboard(request):
    productos = Producto.objects.all()

    context = {'productos': productos}
    return render(request,"core/dashboard.html", context)

def chanchito(request, id):
    producto = Producto.objects.get(id=id)

    context = {'producto': producto}
    return render(request, 'core/detalle.html', context)

@require_POST
def actualizarCarrito(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    producto = Producto.objects.get(id=productId)
    order,creada = Boleta.objects.get_or_create(cliente=request.user,completada=False)
    detalle_orden,creada = Detalle_boleta.objects.get_or_create(boleta=order,producto=producto)
    if action == 'add':
        if detalle_orden.cantidad_productos < producto.stock: 
            detalle_orden.cantidad_productos +=1
    elif action == 'remove': 
        detalle_orden.cantidad_productos -=1
    
    elif action == 'delete':
        detalle_orden.cantidad_productos = 0    
    detalle_orden.save()          
    if detalle_orden.cantidad_productos <= 0: 
        detalle_orden.delete()
    return JsonResponse("Chanchito actualizado",safe=False)          


