from django.db import models
from django.conf import settings

from django.utils import timezone

# Create your models here.
from PIL import Image
from django.core.exceptions import ValidationError


def conversion_fecha(fecha_local):
    """
    Convierte una fecha UTC a la zona horaria local.
    
    Args:
        fecha_local: Objeto datetime para convertir.
        
    Returns:
        Datetime en la zona horaria local.
    """
    return timezone.localtime(fecha_local)




class CategoriaArticulo(models.Model):
    """
    Modelo para las categorías de artículos disponibles en la tienda.
    Permite clasificar productos por género: Hombre o Mujer.
    """
    
    CATEGORIA_OPCIONES=[
        ("H","Hombre"),
        ("M","Mujer")
    ]
    
    
    nombre=models.CharField(choices=CATEGORIA_OPCIONES,  verbose_name="Nombre de la categoría", unique=True )
    slug=models.SlugField(null=True, unique=True, blank=True)



    def __str__(self):
        return f'{self.nombre}'
    


class Talla(models.Model):
    """
    Modelo que almacena los valores de tallas disponibles para los productos.
    Ejemplos: S, M, L, XL, XXL, etc.
    """
    valor=models.CharField(max_length=10, null=True, help_text="Ingrese el valor de la talla (L,M,S,XL, etc... )", unique=True )


    def __str__(self):
        return f'{self.valor}'
    
    class Meta:
        
        verbose_name_plural="Tallas"
       




class Articulo(models.Model):
    """
    Modelo principal de producto en la tienda.
    Contiene información general del producto como nombre, descripción,
    categoría, disponibilidad e imagen principal.
    """

    nombre=models.CharField(max_length=100, unique=True, verbose_name="Nombre del artículo")
    
    disponible=models.BooleanField(default=True,  help_text="Marca si el producto está disponible para compra")

    descripcion=models.TextField(max_length=500, blank=True, verbose_name="Descripción")


    categoria=models.ForeignKey(CategoriaArticulo, on_delete=models.CASCADE, null=True, verbose_name="Categoría del artículo", related_name="articulos")

    destacado=models.BooleanField(default=False, verbose_name="Producto destacado", help_text="Marcar para mostrar en página principal")

    imagen_articulo=models.ImageField(upload_to="articulos/imagenes/", verbose_name="Imagen del artículo", help_text="Esta será la imagen principal del artículo", null=True, max_length=255)

   

    class Meta:
        db_table="articulo"
        verbose_name_plural="Artículos"
        
        
    @property
    def tiene_variantes(self):
        """Verifica si el artículo tiene variantes (tallas) definidas."""
        return self.variante_articulo.exists()
    
    @property
    def tiene_stock(self):
        """Verifica si el artículo tiene al menos una variante en stock."""
        return self.variante_articulo.filter(stock__gt=0).exists()

        
  
    def clean(self):
        """Valida que la imagen tenga dimensiones mínimas y el límite de destacados."""
        if self.imagen_articulo:
            if not self.validar_dimensiones():
                raise ValidationError("La imagen debe ser de al menos 416x350")
            
        
        if self.destacado:
            self.validar_destacados()
        
    def validar_destacados(self):
        """Valida que no haya más de 6 productos destacados simultáneamente."""
            
        
        
        articulos_destacados = Articulo.objects.filter(destacado=True)

        if self.pk:
            articulos_destacados=articulos_destacados.exclude(pk=self.pk)

        if articulos_destacados.count()>=6:
            raise ValidationError("No pueden haber más de 6 artículos destacados")
           
        
    def validar_dimensiones(self):
        img = Image.open(self.imagen_articulo)
        resultado = img.height >= 416 and img.width >= 350
        self.imagen_articulo.seek(0)  # ← resetea el cursor al inicio
        return resultado
    


    def __str__(self):
     return f'{self.nombre} '
    
    

class VarianteArticulo(models.Model):
    """
    Modelo que representa una variante específica de un artículo.
    Cada variante corresponde a una combinación de artículo + talla,
    con su propio stock y precio.
    """
    articulo=models.ForeignKey(Articulo, on_delete=models.CASCADE, related_name="variante_articulo")
    stock=models.PositiveIntegerField(default=0 , verbose_name="Stock disponible")
    talla=models.ForeignKey(Talla, on_delete=models.CASCADE, null=True)
    precio=models.DecimalField(null=True,decimal_places=0, max_digits=12, verbose_name="Precio base del artículo", help_text="Sin puntos ni comas")
   


    def __str__(self):
        return f'{self.articulo}, Talla: {self.talla}'
    
    class Meta:
        unique_together=['articulo', 'talla']


    @property
    def esta_disponible(self):
        """Verifica si esta variante tiene stock disponible."""
        return self.stock>0




class ImagenArticulo(models.Model):
    """
    Modelo para almacenar imágenes secundarias de los artículos.
    Un artículo puede tener múltiples imágenes para mostrar diferentes vistas.
    """
    imagenes=models.ImageField(upload_to="articulos/imagenes/",verbose_name="Imágenes del artículo", help_text="Estas serán las imágenes secundarias del artículo")
    articulo=models.ForeignKey(Articulo, on_delete=models.CASCADE, verbose_name="Artículo", related_name="imagenes")

    class Meta:
        verbose_name_plural="Imágenes de artículo"

    
    def __str__(self):
        return f'{ self.imagenes}'









    


    


