from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Pedido, PedidoItem
# Register your models here.
@admin.register(Pedido)
class PedidoAdmin(ModelAdmin):
    """Admin para gestionar pedidos. Permite ver estado, usuario, fecha y total. Opción de cambiar estado."""
    list_display=['numero_pedido','usuario', 'estado', 'fecha_pedido', 'total', 'nombre_envio', 'apellido_envio', 'direccion_envio', 'datos_adicionales_envio', 'telefono_envio']
    list_editable=['estado']
    search_fields=['numero_pedido']
    

@admin.register(PedidoItem)
class PedidoItemAdmin(ModelAdmin):
    """Admin para ver los artículos individuales dentro de cada pedido."""
    list_display=['variante_articulo', 'pedido', 'cantidad', 'precio']