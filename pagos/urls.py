from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('pago_exitoso/', views.pago_exitoso, name="pago_exitoso"),
    path('pago_fallido/', views.pago_fallido, name="pago_fallido"),
    path('pago_pendiente/', views.pago_pendiente, name="pago_pendiente")
 
]