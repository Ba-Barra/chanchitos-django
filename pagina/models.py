from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager,PermissionsMixin
import uuid



# Create your models here.
class  CustomUserManager(UserManager):
    def _create_user(self, email ,password,**extra_fields):
        if not email:
            raise ValueError('Email invalido')
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_user(self, email=None, password=None, **extra_fields):

        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email,password,**extra_fields)

    def create_superuser(self,email=None,password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email,password,**extra_fields)


class Usuario (AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    rut = models.CharField(max_length=10,unique=True,primary_key=True,verbose_name='Rut')
    nombre = models.CharField(max_length=250)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta: 
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Producto (models.Model):
    TIPO = [
        ('C', 'Chanchito'),
        ('P', 'Paila')
    ]
    tipo = models.CharField(max_length=1,choices=TIPO, default= 'C')
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    nombre = models.CharField(max_length=50,unique=True)
    descripcion = models.CharField(max_length=300)
    valor = models.IntegerField() 
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to="productos/")
    
    def __str__(self):
        return str(self.id)
    @property
    def get_image_url(self):
        try: 
            return self.imagen.url
        except: 
            return ""
    

class Boleta (models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    fechaVenta = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    completada = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)
    @property
    def get_total(self):
        detalle = self.detalle_boleta_set.all()
        total = sum([item.producto.valor * item.cantidad_productos for item in detalle])
        return total
    @property
    def get_item(self):
        detalle = self.detalle_boleta_set.all()
        total = sum([item.cantidad_productos for item in detalle])
        return total
    @property
    def get_envio(self):
        envio = 5000
        total = self.get_total + envio
        return total
    
class Detalle_boleta (models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    boleta = models.ForeignKey(Boleta, on_delete=models.CASCADE)
    cantidad_productos = models.IntegerField(default=0) 
    def __str__(self):
        return str(self.boleta.id) + '-' + self.producto.nombre
    @property
    def get_total(self):
        total = self.producto.valor * self.cantidad_productos
        return total
    
   
class Region (models.Model):
    nombre = models.CharField(max_length=100)

class Envio (models.Model):
    envio = [
        ('E', 'Enviado'),
        ('C', 'Camino'),
        ('R', 'Recibido'),
        ('N', 'No Recibido'),
        ('P', 'Preparacion')
    ]
    boleta = models.OneToOneField(Boleta,on_delete=models.CASCADE)
    region = models.ForeignKey(Region,on_delete=models.SET_NULL,blank=True, null=True)
    direccion = models.CharField(max_length=250)
    estado = models.CharField(max_length=1,choices=envio,default= 'P')
    @property
    def get_estado (self):
        return self.get_estado_display()
    @property
    def get_direccion(self):
        return self.direccion + " " + self.region.nombre



    














