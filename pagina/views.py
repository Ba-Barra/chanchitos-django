from django.shortcuts import render, redirect
from .models import Producto, Boleta, Detalle_boleta, Region, Envio, Usuario
from django.views.decorators.http import require_POST
import json
from django.http import JsonResponse , HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
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
    boletas = Boleta.objects.filter(completada=True,cliente=request.user)
    context = {'boletas': boletas}

    return render(request,"core/pedidos_usuario.html",context)


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

@login_required
@permission_required("pagina.view_user",raise_exception=True) ##Tira un error en caso q no exista permiso para acceder 
def dashboard(request):
    tipos = Producto.TIPO
    productos = Producto.objects.all()
    if request.method == 'POST':
        tipo = request.POST.get("Tipo")
        nombre = request.POST.get("productonombre")
        precio = request.POST.get("precioProducto")
        descripcion = request.POST.get("descripcionProducto")
        stock = request.POST.get("StockProducto")
        imagen = request.FILES.get("imagenProducto")
        if int(precio) < 0 : 
            messages.error(request,"Precio Chanchi-invalido")
            return redirect('dashboard')
        if int(stock) < 0:
            messages.error(request,"Chanchi-stock invalido")  
            return redirect('dashboard')  
        if Producto.objects.filter(nombre = nombre).exists():
            messages.error(request,"No pueden existir dos chanchitos iguales en el universo")
            return redirect ('dashboard')
        if imagen.name.split('.')[-1] not in ['jpg', 'jpeg', 'png', 'webp', 'svg']:
            messages.error(request, "Chanchi-foto no valida")
            return redirect('dashboard')
        if imagen is None :
            messages.error(request,"No hay chanchi imagen! :(")
            return redirect ('dashboard')
        
        nuevo_producto = Producto.objects.create(tipo = tipo,nombre=nombre,descripcion = descripcion,valor = precio, stock = stock, imagen= imagen)
        nuevo_producto.save()
        messages.success(request,"Chanchi-agregado con éxito!")
        return redirect('dashboard')



    context = {'productos': productos, 'tipos': tipos}
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
   
@login_required
@permission_required("pagina.view_user",raise_exception=True)
def pedidos_admin (request):
    boletas = Boleta.objects.filter(completada=True)
    context = {'boletas': boletas}
    return render(request,"core/pedidos_admin.html",context) 
 
@login_required
@permission_required("pagina.view_user",raise_exception=True)
def detalle_boleta(request,id):
    estados = Envio.envio
    boleta = Boleta.objects.get(id=id)
    productos = Detalle_boleta.objects.filter(boleta=boleta)
    context = {'boleta':boleta,'productos':productos,'estados':estados}
    return render(request,"core/detalle_boleta.html", context)

@login_required
@permission_required("pagina.view_user",raise_exception=True)
def editarProducto(request,id):
    tipos = Producto.TIPO
    producto = Producto.objects.get(id=id)
    if request.method == 'POST':
        tipo = request.POST.get("Tipo")
        nombre = request.POST.get("productonombre")
        precio = request.POST.get("valorProducto")
        descripcion = request.POST.get("descripcionProducto")
        stock = request.POST.get("StockProducto")
        imagen = request.FILES.get("imagenProducto")
        if int(precio) < 0 : 
            messages.error(request,"Precio Chanchi-invalido")
            return redirect('dashboard')
        if int(stock) < 0:
            messages.error(request,"Chanchi-stock invalido")  
            return redirect('dashboard')  
        if Producto.objects.filter(nombre = nombre).exclude(id=id).exists():
            messages.error(request,"No pueden existir dos chanchitos iguales en el universo")
            return redirect ('dashboard')
        if imagen is not None:
            if imagen.name.split('.')[-1] not in ['jpg', 'jpeg', 'png', 'webp', 'svg']:
                messages.error(request, "Chanchi-foto no valida")
                return redirect('dashboard')
            

        producto.tipo = tipo
        producto.nombre = nombre
        producto.valor=precio
        producto.descripcion = descripcion
        producto.stock = stock
        if imagen is not None:
            producto.imagen = imagen
        producto.save()    

        messages.success(request,"Chanchi-editado con éxito!")
        return redirect('dashboard')
    context = {'producto': producto,'tipos': tipos}
    return render(request,"core/editarProducto.html", context)

@login_required
@permission_required("pagina.view_user",raise_exception=True)
def eliminarProducto(request,id):
    producto = Producto.objects.get(id=id)
    if not Producto.objects.filter(id=id).exists():
        messages.error(request,"Chanchi-no existe")
        return redirect('dashboard')
    producto.delete()
    messages.success(request,"Chanchi-elimidado con éxito :(")
    return redirect('dashboard')

@login_required
def misProductos(request):
    boleta = Boleta.objects.filter(cliente=request.user,completada=True).all()
    context = {'boletas': boleta}
    return render(request,"core/misProductos.html",context)

@login_required
def productos_usuario(request,id):
    boleta = Boleta.objects.get(id=id)
    productos = Detalle_boleta.objects.filter(boleta=boleta)
    if not boleta.cliente == request.user or not request.user.is_staff:
        return redirect('index')
    context = {'boleta':boleta,'productos':productos}
    return render(request,"core/productos_usuario.html", context)
    
@require_POST
def editarEnvio(request):
    data = json.loads(request.body)
    id = data['id']
    status = data['status']
    boleta = Boleta.objects.get(id=id)
    envio = Envio.objects.get(boleta=boleta)
    if envio is None:
        return HttpResponse({'message': 'El Chanchi-envio no existe'}, status=404)
    
    envio.estado = status
    envio.save()
    return HttpResponse({'message': 'Chanchi-envio actualizado correctamente'}, status=200)

@login_required
@permission_required("pagina.view_user",raise_exception=True)
def usuarios(request):
    usuario = Usuario.objects.all()
    context = {'usuarios': usuario}


    return render(request,"core/usuarios.html",context)

@login_required
@permission_required("pagina.view_user",raise_exception=True)
def editarUsuario(request,id):
    usuario = Usuario.objects.get(rut=id)
    if request.method == 'POST':
        email = request.POST.get("usuarioEmail")
        nombre = request.POST.get("usuarioNombre")
        if Usuario.objects.filter(email = email).exclude(rut=id).exists():
            messages.error(request,"No pueden existir dos chanchi-usuarios iguales en el universo")
            return redirect ('dashboard')
        if email == "":
            messages.error(request,"Pone un chanchi-correo po!")
            return redirect ('dashboard')
        if nombre == "":
            messages.error(request,"El chanchi-nombre no puede ser vacio")
            return redirect('dashboard')
        
        usuario.email = email
        usuario.nombre = nombre
        usuario.save()    
        messages.success(request,"Chanchi-editado con éxito!")
        return redirect('dashboard')
    context = {'usuario': usuario}
    return render(request,"core/editarUsuario.html", context)

@login_required
@permission_required("pagina.view_user",raise_exception=True)
def eliminarUsuario(request,id):
    usuario = Usuario.objects.get(rut=id)
    if not Usuario.objects.filter(rut=id).exists():
        messages.error(request,"El chanchi-usuario no existe")
        return redirect('dashboard')
    usuario.delete()
    messages.success(request,"Chanchi-elimidado con éxito :(")
    return redirect('dashboard')








