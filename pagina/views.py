from django.shortcuts import render

# Create your views here.
def index(request):
    return render (request,"core/index.html")

def productos(request):
    return render(request, "core/productos.html")

def registrar(request):
    return render(request, "core/registrar.html")

def login(request):
    return render(request,"core/login.html")

def check_out(request):
    return render(request,"core/check_out.html")

def pedidos_usuario(request):
    return render(request,"core/pedidos_usuario.html")

def carrito(request):
    return render(request, "core/carrito.html")

def dashboard(request):
    return render(request,"core/dashboard.html")