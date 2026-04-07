from django.urls import path
from .import views

urlpatterns = [
 path("lista_pedidos", views.lista_pedidos, name="lista_pedidos"),
 path("detalle_pedido/<int:pedido_id>/", views.detalle_pedido, name="detalle_pedido"),
 path("cancelar_pedido/<str:numero_pedido>", views.cancelar_pedido, name="cancelar_pedido")

]