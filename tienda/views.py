from django.shortcuts import render, redirect
from .models import *
from usuarios.forms import IniciarSesionForm
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.

def index(request):
    """Vista de página de inicio. Muestra los artículos destacados."""
    articulos_destacados=Articulo.objects.filter(destacado=True)
    
   
    return render(request,"index/index.html", {
        "form":IniciarSesionForm(),
        "articulos_destacados":articulos_destacados,
       
        })




def detalle_producto(request, producto_id):
    """Vista que muestra los detalles completos de un producto."""
    producto=get_object_or_404(Articulo, id=producto_id)
    imagenes_producto=producto.imagenes.all()
    
    talla_variantes=producto.variante_articulo.select_related('talla')
    
    
    return render(request, "productos/detalle_producto.html",{
        "producto":producto,
        "imagenes_producto":imagenes_producto,
        "talla_variantes":talla_variantes,
       
        
    })




def categoria_hombres(request):
    """Vista de productos para Hombres con búsqueda y paginación."""
    query=request.GET.get('q','')
    pagina_obj = None
    
    try:
        
        categoria=CategoriaArticulo.objects.get(nombre="H")
    
        articulos_hombre=categoria.articulos.all()
    
        if query:
            articulos_hombre=articulos_hombre.filter(Q(nombre__unaccent__icontains=query))
        

    
        paginador=Paginator(articulos_hombre, 20)
        numero_pagina=request.GET.get('pagina')
        pagina_obj=paginador.get_page(numero_pagina)
    
    except CategoriaArticulo.DoesNotExist:
        categoria=None
    
        
    
    return render(request, "productos/categoria_hombre.html",{
        "categoria":categoria,
        "pagina_obj":pagina_obj,
        "query":query
        
    })
    
    
    
def categoria_mujer(request):
    """Vista de productos para Mujeres con búsqueda y paginación."""
    query = request.GET.get('q', '')
    pagina_obj = None

    try:
        categoria = CategoriaArticulo.objects.get(nombre="M")
        articulos_mujer = categoria.articulos.all()

        if query:
            articulos_mujer = articulos_mujer.filter(Q(nombre__unaccent__icontains=query))

        paginador = Paginator(articulos_mujer, 20)
        numero_pagina = request.GET.get('pagina')
        pagina_obj = paginador.get_page(numero_pagina)

    except CategoriaArticulo.DoesNotExist:
        categoria = None  # ✅ el template captura esto

    return render(request, "productos/categoria_mujer.html", {
        "categoria": categoria,
        "pagina_obj": pagina_obj,
        "query": query
    })