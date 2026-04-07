from django import forms
from .models import Pedido  
import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

PATRON_LETRAS = r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$'


PATRON_TELEFONO=r'^\d{7,10}$'

class PedidoForm(forms.ModelForm):
    """Formulario para recopila información de envío durante el checkout.
    Valida que los datos sean correctos (nombres sin números, teléfono válido, dirección adecuada).
    """
    
   
     
    class Meta:
     model=Pedido
     fields=['nombre_envio','apellido_envio', 'direccion_envio', 'datos_adicionales_envio',  'telefono_envio']
     labels={
         'nombre_envio':"Nombre",
         'apellido_envio':"Apellido",
         'direccion_envio':"Dirección de residencia",
         "datos_adicionales_envio":"Datos adicionales de residencia",
         "telefono_envio":"Teléfono"
     }
    
     
     widgets={
         'nombre_envio':forms.TextInput(
             attrs={'id':'nombre_envio','class':'form-control', 'autofocus':True, 'placeholder':"Ingresa tu nombre"},
            
            
             
         ),
         'apellido_envio':forms.TextInput(
             attrs={'id':'apellido_envio','class':'form-control'}
         ),
         'direccion_envio':forms.TextInput(
             attrs={'id':'direccion_envio','class':'form-control', 'placeholder':"Ej: Calle 38 # 45-33"}
         ),
         
          'datos_adicionales_envio':forms.TextInput(
             attrs={'id':'datos_adicionales_envio','class':'form-control', 'placeholder':"Ej: Apartamento 202, edificio TW Towers"}
         ),
         'telefono_envio':forms.TextInput(
             attrs={'id':'telefono_envio','class':'form-control'}
         ),
        
     }
     
    def clean_nombre_envio(self):
        """Valida que el nombre contenga solo letras y tenga más de 2 caracteres."""
        nombre=self.cleaned_data.get('nombre_envio', '').strip()
        if not re.match(PATRON_LETRAS, nombre):
            raise ValidationError("¡El nombre solo puede contener letras o espacios!")
        
        if len(nombre)<=2:
            raise ValidationError("¡El nombre debe de contener más de dos letras!")
        return nombre
        
        
    def clean_apellido_envio(self):
        """Valida que el apellido contenga solo letras y tenga más de 3 caracteres."""
        apellido=self.cleaned_data.get('apellido_envio', '').strip()
        
        if not re.match(PATRON_LETRAS, apellido):
            raise ValidationError("¡El apellido solo puede contener letras o espacios!")
        
        if len(apellido)<=3:
            raise ValidationError("¡El apellido debe contener más de tres letras!")
        
        return apellido
    
    def clean_telefono_envio(self):
        """Valida que el teléfono tenga entre 7 y 10 dígitos."""
        telefono=self.cleaned_data.get('telefono_envio', '').strip()
        
        if not re.match(PATRON_TELEFONO, telefono):
            raise ValidationError("¡Ingrese un teléfono válido!")
        
        return telefono
    
    def clean_direccion_envio(self):
        """Valida que la dirección tenga al menos 5 caracteres."""
        direccion=self.cleaned_data.get('direccion_envio', '').strip()
        
        if len(direccion)<5:
            raise ValidationError("¡La dirección debe contener al menos 5 caracteres!")
        
        return direccion
    
    def clean_datos_adicionales_envio(self):
        """Valida que los datos adicionales tengan al menos 3 caracteres."""
        datos_adicionales=self.cleaned_data.get('datos_adicionales_envio', '').strip()
        
        if len(datos_adicionales)<3:
            raise ValidationError("¡Los datos adicionales deben tener al menos 3 caracteres!")
        
        return datos_adicionales