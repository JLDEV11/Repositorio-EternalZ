from django.contrib import admin
from . models import *
from unfold.admin import ModelAdmin
from django.utils.html import format_html
# Register your models here.



    
class ImagenArticuloInline(admin.StackedInline):
    """Permite agregar imágenes inline al editar un artículo en el admin."""
    model = ImagenArticulo
  

@admin.register(Articulo)
class ArticuloAdmin(ModelAdmin):
    """Admin para gestionar artículos. Permite marcar como destacados y subir imágenes."""
    list_display=['id','nombre','disponible','descripcion','destacado']
    list_editable=['destacado']
    search_fields=['id','nombre']
    inlines=[ImagenArticuloInline]
    
    
    
    

@admin.register(Talla)
class TallaAdmin(ModelAdmin):
    """Admin para gestionar las tallas disponibles (S, M, L, XL, etc)."""
    list_display=['id','valor']
    search_fields=['valor']


@admin.register(CategoriaArticulo)
class CategoriaAdmin(ModelAdmin):
    """Admin para gestionar categorías de artículos (Hombre, Mujer)."""
    list_display=['id','nombre']
    search_fields=['nombre']


@admin.register(VarianteArticulo)
class VarianteArticuloAdmin(ModelAdmin):
    """Admin para gestionar variantes de artículos (artículo + talla + precio + stock)."""
    list_display=['id','articulo','stock', 'talla', 'precio']
    search_fields=['articulo']
    

@admin.register(ImagenArticulo)
class ImagenArticuloAdmin(ModelAdmin):
    """Admin para gestionar imágenes secundarias de artículos."""
    list_display=['imagenes','articulo']
    search_fields=['articulo']