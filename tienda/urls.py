from django.urls import path
from . import views

urlpatterns=[
    path('',views.index, name="index"),
    path('detalle_producto/<int:producto_id>/', views.detalle_producto, name="detalle_producto" ),
    path('categoria_hombre', views.categoria_hombres, name="categoria_hombre" ),
    path('categoria_mujer', views.categoria_mujer, name="categoria_mujer" ),

]