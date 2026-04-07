from django.urls import path
from . import views

urlpatterns=[
    path('carrito_compras', views.carrito_compras, name="carrito_compras" ),
    path('agregar_carrito', views.agregar_al_carrito, name="agregar_carrito"),
    path('eliminar_carrito/<int:articulo_id>/', views.eliminar_carrito, name="eliminar_carrito"),
    path('limpiar_carrito', views.limpiar_carrito, name="limpiar_carrito"),
    path('carrito/actualizar/<int:variante_id>/', views.actualizar_cantidad, name='actualizar_cantidad'),


    
]