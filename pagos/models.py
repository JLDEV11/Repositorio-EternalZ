from django.db import models
from django.conf import settings
from tienda.models import conversion_fecha, Articulo
from pedidos.models import Pedido
# Create your models here.



class Pago(models.Model):
    """Modelo que registra los pagos procesados a través de Mercado Pago.
    Contiene ID del pago, estado (completado, pendiente, fallido) y detalles de la transacción.
    """

    ESTADO_OPCIONES=[
        ("C","Completado"),
        ("P","Pendiente"),
        ("F","Fallido")
    ]
    
    payment_id = models.CharField(max_length=100, unique=True, null=True, verbose_name="ID del pago")
    pedido=models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name="pago", null=True)
    usuario=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_pago=models.DateTimeField(auto_now_add=True, verbose_name="Fecha del pago")
    tipo_pago=models.CharField(max_length=50, verbose_name="Tipo de pago")
    estado=models.CharField(max_length=1, choices=ESTADO_OPCIONES, default="P")
    total = models.DecimalField(max_digits=10, decimal_places=2)
    


    class Meta:
        db_table="pago"
        verbose_name_plural="Pagos"


    def __str__(self):
        fecha_local=conversion_fecha(self.fecha_pago)
        return f'{self.tipo_pago} - {self.get_estado_display()} -{ fecha_local.strftime("%A %d de %B de %Y a las %H:%M").capitalize()} '



    
