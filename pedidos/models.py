from django.db import models
import random
import uuid

from django.conf import settings
# Create your models here.
from tienda.models import VarianteArticulo

def numero_pedido():
    """Genera un número de pedido único basado en UUID de 8 caracteres en mayúsculas."""
    return uuid.uuid4().hex[:8].upper() 


class Pedido(models.Model):
    """Modelo que representa un pedido de compra realizado por un usuario.
    Contiene información de envío, estado del pedido y total.
    """
    
    ESTADO_OPCIONES = [
        ("P", "Pendiente"),
        ("E", "Enviado"),
        ("G", "Entregado"),
        ("X", "Cancelado"),
    ]
    
    numero_pedido=models.CharField(default=numero_pedido, unique=True , verbose_name="Número de pedido")
    usuario=models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE, related_name="pedidos", null=True)
    estado=models.CharField(choices=ESTADO_OPCIONES, default="P", max_length=1)
    nombre_envio=models.CharField(max_length=50, verbose_name="Nombre asociado al envío")
    apellido_envio=models.CharField(max_length=100, verbose_name="Apellido asociado al envío")
    direccion_envio=models.CharField(max_length=50, verbose_name="Dirección asociada al envío")
    datos_adicionales_envio=models.CharField(max_length=50, verbose_name="Datos adicionales del envío")
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    fecha_pedido=models.DateTimeField(auto_now_add=True, null=True)
    telefono_envio=models.CharField(max_length=50, verbose_name="Teléfono asociado al envío")
    
    class Meta:
        db_table = "pedido"
        verbose_name_plural = "Pedidos"
    
    def __str__(self):
         return f"Pedido #{self.id} - {self.usuario}"
    
    
    
    
   
class PedidoItem(models.Model):
    """Modelo que representa un artículo dentro de un pedido.
    Almacena la referencia al artículo, cantidad y precio al momento de la compra.
    """
    pedido=models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="pedido_items")
    variante_articulo=models.ForeignKey(VarianteArticulo, on_delete=models.CASCADE, related_name="variantes", null=True, verbose_name="Variante de artículo")
    cantidad=models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)