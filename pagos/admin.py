from django.contrib import admin
from .models import *
from unfold.admin import ModelAdmin
# Register your models here.

@admin.register(Pago)
class PagoAdmin(ModelAdmin):
    """Admin para ver registros de pagos procesados. Muestra ID pago, estado, usuario y total."""
    list_display=['payment_id', 'total', 'fecha_pago', 'tipo_pago','pedido']

    search_fields=['payment_id', 'usuario']
        
        
