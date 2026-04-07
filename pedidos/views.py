from django.shortcuts import render,redirect, get_object_or_404
from .forms import PedidoForm
from .models import Pedido
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.db.models import F
# Create your views here.

@login_required
def lista_pedidos(request):
    """Muestra el listado de todos los pedidos del usuario autenticado."""
    
    pedidos=Pedido.objects.filter(usuario=request.user).all()
    
    for pedido in pedidos:
        if pedido.estado=="X":
            pass
            
            
    
    return render(request, "lista_pedidos.html", {
        "pedidos":pedidos
    })
    
    
def detalle_pedido(request, pedido_id):
    """Muestra los detalles completos de un pedido específico incluyendo sus artículos."""
    pedido=get_object_or_404(Pedido, id=pedido_id)
    items=pedido.pedido_items.all()
   
    return render(request, "detalle_pedido.html",{
        "pedido":pedido,
        "items":items
    })
    
    
@login_required
def cancelar_pedido(request, numero_pedido):
    """Cancela un pedido pendiente. Solo permite cancelación si el estado es 'Pendiente'."""
    pedido = get_object_or_404(Pedido, numero_pedido=numero_pedido, usuario=request.user)
    
    items = pedido.pedido_items.select_related('variante_articulo')
    
    
    # Solo se puede cancelar si está pendiente
    if request.method=="POST":
        if pedido.estado != "P":
            
            return redirect('lista_pedidos')
        

   
        for item in items:
            variante = item.variante_articulo
            variante.stock = F('stock') + item.cantidad
            variante.save()
        
    
        pedido.estado = "X"  # Cancelado
        pedido.save()
      
        return redirect('lista_pedidos')
        
   
        