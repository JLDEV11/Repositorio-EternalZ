from django.db import models
from django.conf import settings
# Create your models here.
from tienda.models import Articulo, VarianteArticulo


class Carrito(models.Model):
    """Carrito asociado a un usuario."""

    usuario=models.OneToOneField(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE, related_name="carrito")

    creado=models.DateTimeField(auto_now_add=True)
    actualizado=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Carrito de {self.usuario.email}'
    
    @property
    def total_items(self):
        """Cantidad total de artículos en el carrito"""
        return sum(item.cantidad for item in self.items.all())
    
    @property
    def total_precio(self):
        """Precio total del carrito"""
        return sum(item.subtotal() for item in self.items.all())
    
class ItemCarrito(models.Model):
   """Elemento individual del carrito (Un artículo y su cantidad)"""
   carrito=models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
   variante_articulo=models.ForeignKey(VarianteArticulo, on_delete=models.CASCADE)
   cantidad=models.PositiveIntegerField(default=1)

   class Meta:
       unique_together=('carrito','variante_articulo')

   def __str__(self):
        return f'{self.variante_articulo.articulo.nombre} x {self.cantidad}'
   
   def subtotal(self):
       return self.variante_articulo.precio* self.cantidad