from django.contrib import admin
from .models import *
from unfold.admin import ModelAdmin
# Register your models here.



@admin.register(Carrito)
class CarritoAdmin(ModelAdmin):
    """Admin para ver carritos de usuarios. Muestra total de items y precio total."""
    
    list_display=['usuario','creado', 'actualizado']
    search_fields=['usuario']


@admin.register(ItemCarrito)
class CarritoItemAdmin(ModelAdmin):
    """Admin para ver los artículos individuales en cada carrito."""
    list_display=['carrito','variante_articulo', 'cantidad']
    search_fields=['carrito', 'variante_articulo']

    