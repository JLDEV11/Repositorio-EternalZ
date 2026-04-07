"""
Configuración del cliente SDK de Mercado Pago.
Inicializa la conexión con Mercado Pago usando el token de acceso desde settings.
"""
import mercadopago
from django.conf import settings

sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)