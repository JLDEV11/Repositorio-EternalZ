# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from carrito.models import Carrito, ItemCarrito
from pagos.models import *
from .mercadopago_client import sdk
from django.contrib import messages
from pedidos.forms import PedidoForm
from pedidos.models import Pedido, PedidoItem
from django.db.models import F
from tienda.models import VarianteArticulo

@login_required
def checkout(request):
    """Vista de checkout: recopila datos de envío y redirige a Mercado Pago para pagar.
    Crea el pedido y decrementa stock al procesar el formulario.
    """
    
    carrito = get_object_or_404(Carrito, usuario=request.user)
    items = carrito.items.select_related('variante_articulo').all()

    if not items.exists():
        return redirect('carrito_compras')
    
   

    form = PedidoForm()

    if request.method == "POST":
        form=PedidoForm(request.POST)
        if form.is_valid():
            
            request.session['datos_envio'] = form.cleaned_data
                

            articulos = []
            for item in items:
                articulos.append({
                    "title": item.variante_articulo.articulo.nombre,
                    "quantity": item.cantidad,
                    "unit_price": float(item.variante_articulo.precio),
                    "currency_id": "COP"
                })

            preference_data = {
                "items": articulos,
                "back_urls": {
                    "success": f"{settings.BASE_URL}/pago_exitoso/",
                    "failure": f"{settings.BASE_URL}/pago_fallido/",
                    "pending": f"{settings.BASE_URL}/pago_pendiente/"
                },
                "auto_return": "approved",
               
            }

            preference_response = sdk.preference().create(preference_data)
            preference = preference_response["response"]

            return redirect(preference['sandbox_init_point'])

    return render(request, 'pagos/checkout.html', {
        'form': form,
        'carrito': carrito,
        'items': items,
    })



@login_required
def pago_exitoso(request):
    payment_id = request.GET.get('payment_id')

    if not payment_id:
        return redirect('index')

    payment_info = sdk.payment().get(payment_id)
    response = payment_info["response"]
    status = response["status"]
    tipo_pago = response["payment_type_id"]

    if status != "approved":
        messages.error(request, "El pago no fue aprobado.")
        return redirect('checkout')

  
    datos_envio = request.session.get('datos_envio')
    if not datos_envio:
        return redirect('checkout')

    carrito = get_object_or_404(Carrito, usuario=request.user)
    items=carrito.items.select_related('variante_articulo').all()

    pago_existente = Pago.objects.filter(payment_id=payment_id).first()
    if pago_existente:
        return render(request, 'pagos/pago_exitoso.html', {
            'payment_id': payment_id,
            'pedido': pago_existente.pedido
        })

           
    pedido = Pedido.objects.create(
                usuario=request.user,
                total=carrito.total_precio,
                estado='P',
                nombre_envio=datos_envio['nombre_envio'],
                apellido_envio=datos_envio['apellido_envio'],
                direccion_envio=datos_envio['direccion_envio'],
                telefono_envio=datos_envio['telefono_envio'],
                datos_adicionales_envio=datos_envio['datos_adicionales_envio']
                
            )

            # Crear PedidoItems y descontar stock
    for item in items:
                PedidoItem.objects.create(
                   pedido = pedido,
                   variante_articulo = item.variante_articulo,
                   cantidad = item.cantidad,
                  precio = item.variante_articulo.precio
                              
                )
                VarianteArticulo.objects.filter(id=item.variante_articulo.id).update(
                    stock=F('stock') - item.cantidad
                )

            # Crear el Pago
    Pago.objects.create(
                payment_id=payment_id,
                usuario=request.user,
                estado='C',
                total=carrito.total_precio,
                tipo_pago=tipo_pago,
                pedido=pedido
            )

            # Vaciar carrito y sesión
    carrito.items.all().delete()
    request.session.pop('datos_envio', None)

    

    return render(request, 'pagos/pago_exitoso.html', {
        'payment_id': payment_id,
        'pedido': pedido
    })


def pago_fallido(request):
    """Muestra página de pago fallido cuando la transacción no fue aprobada."""
    return render(request, 'pagos/pago_fallido.html')

def pago_pendiente(request):
    """Muestra página de pago pendiente mientras se procesa la transacción."""
    payment_id = request.GET.get('payment_id')
    return render(request, 'pagos/pago_pendiente.html', {'payment_id': payment_id})