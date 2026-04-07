"""Filtros personalizados para templates de Django."""
from django import template

register = template.Library()

@register.filter
def precio_cop(valor):
    """Formatea un número como precio en Pesos Colombianos (COP).
    Ejemplo: 50000 -> $ 50.000
    """
    try:
        return f"$ {int(valor):,}".replace(",", ".")
    except (ValueError, TypeError):
        return valor