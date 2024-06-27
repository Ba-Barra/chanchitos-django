from django.shortcuts import render, redirect
from .models import Producto, Boleta, Detalle_boleta, Region, Envio 
from django.views.decorators.http import require_POST
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from .forms import LoginForm, RegisterForm

# Create your views here.
def index(request):
    return render (request,"core/index.html")

def productos(request):
    productos = Producto.objects.all()

    context = {'productos': productos}
    return render(request, "core/productos.html", context)

def registrar(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario Chanchi-registrado Chanchi-exitosamente")
            return redirect('login')
        else:
            if form.errors.get('rut') is not None:
                messages.error(request, 'El Chanchi-rut ya se encuentra Chanchi-registrado')
            elif form.errors.get('email') is not None:
                messages.error(request, 'El Chanchi-email ya se encuentra Chanchi-registrado')
            elif form.errors.get('password1') is not None:
                messages.error(request, 'Las Chanchi-contraseñas no Chanchi-coinciden')
            elif form.errors.get('password2') is not None:
                messages.error(request, 'La Chanchi-contraseña es demasiado Chanchi-comun')
            elif form.errors.get('first_name') is not None:
                messages.error(request, 'El Chanchi-nombre es Chanchi-requerido')
            else:
                messages.error(request, 'Chanchi-Error al registrar el Chanchi-usuario')
            return redirect('registrar')
        
    context = {'form': RegisterForm()}
    return render(request, "core/registrar.html",context)

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Chanchi-Bienvenido ' + str(user.nombre) +  '!')

                next = request.GET.get('next')
                if next is not None and next != '':
                    return redirect(next)
                else:
                    return redirect('index')
            else:
                messages.error(request, 'Chanchi-Email o Chanchi-Contraseña incorrectas')
                return redirect('login')
    return render(request,"core/login.html")

@login_required
def cerrar_la_wea(request):
    logout(request)
    messages.success(request, "Chanchi-cerrando sesión")
    return redirect('index')



@login_required
def check_out(request):
    
    order,creada = Boleta.objects.get_or_create(cliente=request.user,completada=False)
    items = order.detalle_boleta_set.all()
    items_carrito = order.get_item

    if items.count() <= 0:
        messages.error(request,"No hay Chanchi-productos en tu Chanchi-carrito")
        return redirect('productos')

    if request.method == 'POST':
        idregion = request.POST.get('Country')
        region = Region.objects.get(pk=idregion)
        direccion = request.POST.get('direccion')
        if not Region.objects.filter(pk=idregion).exists():
            messages.error(request,"Chanchi-Region no Chanchi-encontrada")
            return redirect('check_out')
        if direccion == "":
            messages.error(request,"Chanchi-direccion no Chanchi-válida")
            return redirect('check_out')
        


        Envio.objects.create(boleta=order,region=region,direccion=direccion)
        order.completada = True 
        order.save()
        messages.success(request,"Chanchi-procesada con Chanchi-éxito")
        return redirect('index')

    context = {'items': items, 'order' : order}   
    return render(request,"core/check_out.html", context)

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


