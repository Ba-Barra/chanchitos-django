from django.contrib import admin
from .models import Usuario , Producto , Boleta , Detalle_boleta

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Producto)
admin.site.register(Boleta)
admin.site.register(Detalle_boleta)
