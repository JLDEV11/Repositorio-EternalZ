from .models import CustomUser
from django import forms

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.forms import PasswordResetForm , SetPasswordForm

NOMBRE_APELLIDO_REGEX=r'^[a-zA-ZñÑáéíóúÁÉÍÓÚ ]+$'



class CrearUsuarioForm(UserCreationForm):
    """Formulario para crear un nuevo usuario con email y contraseña."""

    class Meta:
        model=CustomUser
        fields=['nombre','apellido','email','password1','password2']
        widgets={
            'nombre':forms.TextInput(
                attrs={'class':'form-control', 'autofocus':True, 'placeholder':'Ingresa tu nombre'
                       }
            ),
            'apellido':forms.TextInput(
                attrs={'class':'form-control', 'placeholder':'Ingresa tu apellido'
                       }
            ),
            'email':forms.EmailInput(
                attrs={'class':'form-control', 'placeholder':'Ingresa tu correo'
                       }
            ),
          
        }



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].label = 'Contraseña' if fieldname == 'password1' else 'Confirme su contraseña'
            self.fields[fieldname].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingresa tu contraseña'})

    def clean_nombre(self):
        """Valida que el nombre contenga solo letras sin caracteres especiales."""
        nombre=self.cleaned_data.get('nombre', '').strip()

        if not re.fullmatch(NOMBRE_APELLIDO_REGEX, nombre):
            raise ValidationError('El nombre no puede contener caracteres especiales, valores numéricos o espacios en blanco')
        
        return nombre
    
    def clean_apellido(self):
        """Valida que el apellido contenga solo letras sin caracteres especiales."""
        apellido=self.cleaned_data.get('apellido', '').strip()
        if not re.match(NOMBRE_APELLIDO_REGEX, apellido):
            raise ValidationError('El apellido no puede contener caracteres especiales, valores numéricos o espacios en blanco')
        
        return apellido
    
   
    

   
    

class IniciarSesionForm(AuthenticationForm):
    """Formulario para autenticar usuarios utilizando email y contraseña."""

    username=forms.EmailField(label="E-mail",widget=forms.EmailInput(attrs={'id':'username','autofocus':True,'placeholder':"Ingresa la dirección de correo electrónico", 
                                                             'class':'form-control'}))
    password=forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'placeholder':"Ingresa tu contraseña", 'class':'form-control'}))

   

    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        

    
class CustomPasswordResetForm(PasswordResetForm):
    """Formulario personalizado para solicitar restablecimiento de contraseña por email."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ingresa tu correo electrónico',
            'required':'required',
        })
       
        
class CustomPasswordResetConfirmView(SetPasswordForm):
    """Formulario para confirmar y establecer una nueva contraseña."""
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user,*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({
            'class':'form-control',
            'placeholder':'Ingresa tu contraseña nueva',
        })
   
        self.fields['new_password2'].widget.attrs.update({
            'class':'form-control',
            'placeholder':'Confirma tu contraseña nueva',
        })
   

    

    