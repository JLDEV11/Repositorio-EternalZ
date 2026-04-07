from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from tienda.models import  VarianteArticulo
from . models import Carrito, ItemCarrito
from django.contrib import messages
from django.core.exceptions import ValidationError
# Create your views here.


@login_required
def agregar_al_carrito(request):
    """Agrega un artículo al carrito del usuario autenticado.
    Requiere: talla seleccionada, cantidad e ID del producto.
    """
    #Encontrar el artículo
   
    
    if request.method == "POST":
                
        
        variante_talla=request.POST.get('variante_talla')
        cantidad=request.POST.get('cantidad_agregada')
        producto_id=request.POST.get('producto_id')

        
        if not variante_talla:
            messages.error(request, "Tienes que seleccionar una talla!")
            return redirect(reverse('detalle_producto', kwargs={"producto_id":producto_id}))
        
        if not cantidad:
            messages.error(request, "Debes seleccionar una cantidad")
            return redirect(reverse('detalle_producto', kwargs={"producto_id":producto_id}))
        
        
        articulo=get_object_or_404(VarianteArticulo, id=variante_talla)
        
        if not articulo.esta_disponible:
            messages.error(request, "Lo sentimos, esta talla está agotada.")
        
            return redirect(reverse('detalle_producto', kwargs={"producto_id": articulo.articulo.id}))
        #Buscar si el usuario ya tiene un carrito, de lo contrario, crear uno automáticamente
        carrito, _=Carrito.objects.get_or_create(usuario=request.user)

        item, creado=ItemCarrito.objects.get_or_create(carrito=carrito, variante_articulo=articulo)
        cantidad_agregada = int(request.POST.get("cantidad_agregada", 1))
        
        if item.variante_articulo.stock<cantidad_agregada:
            messages.error(request, "No hay suficientes artículos en stock, intenta reducir la cantidad")
    
        
        else:
        
            if not creado:
                item.cantidad += cantidad_agregada
                
            else:
                item.cantidad=cantidad_agregada
         
        
            item.save()
    
            messages.success(request, "¡El producto fue añadido al carrito!")

        return redirect(reverse('detalle_producto', kwargs={"producto_id":articulo.articulo.id}))
    
    return redirect('index') 




@login_required
def carrito_compras(request):
    """Muestra el carrito de compras del usuario con todos los artículos y total."""
    carrito, _=Carrito.objects.get_or_create(usuario=request.user)
    items=carrito.items.select_related('variante_articulo')
    total=carrito.total_precio
    
    return render(request,"carrito/carrito_compras.html",{
        "carrito":carrito,
        "items":items,
        "total":total
    })


@login_required
def eliminar_carrito(request, articulo_id):
    """Elimina un artículo específíco del carrito."""
    carrito, _=Carrito.objects.get_or_create(usuario=request.user)
    item=carrito.items.filter(variante_articulo_id=articulo_id).first()
    if item:
        item.delete()
    messages.success(request, "¡El elemento fue eliminado del carrito!")

    return redirect("carrito_compras")


@login_required
def limpiar_carrito(request):
    """Vacía completamente el carrito eliminando todos los artículos."""
    carrito ,_ = Carrito.objects.get_or_create(usuario=request.user)
    carrito.items.all().delete()
    
    if carrito:
        messages.success(request, "¡El carrito fue vaciado con éxito!")
    return redirect("carrito_compras")


@login_required
def actualizar_cantidad(request, variante_id):
    if request.method == "POST":
        cantidad = int(request.POST.get('cantidad', 1))
        carrito = get_object_or_404(Carrito, usuario=request.user)
        item = get_object_or_404(ItemCarrito, carrito=carrito, variante_articulo__id=variante_id)

        if cantidad < 1:
            item.delete()
            messages.success(request, "Producto eliminado del carrito.")
        else:
            item.cantidad = cantidad
            item.save()

    return redirect('carrito_compras')