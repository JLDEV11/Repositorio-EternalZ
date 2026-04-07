from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class CustomUserManager(BaseUserManager):
    """Gestor personalizado de usuarios autenticados por email."""

    def create_user(self, email, password=None, **extra_fields ):
        """Crea y guarda un nuevo usuario con email y contraseña encriptada."""
        #Esto valida si el email es adecuado
        if not email:
            raise ValueError("El correo electrónico es inválido ")
        
        
        
        
        
        #Normaliza el email estandarizando mayúsculas y minúsculas
        email=self.normalize_email(email)
        user=self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
   
    
    def create_superuser(self,email, password=None, **extra_fields):
        """Crea un usuario administrador con permisos máximos."""

        extra_fields.setdefault('is_staff',True)
        
        extra_fields.setdefault('is_superuser',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("El superusuario debe tener is_staff=True")
         
        if extra_fields.get('is_superuser')is not True:
             raise ValueError("El superusuario debe tener is_superuser=True")
        

        return self.create_user(email,password, **extra_fields)

   


class CustomUser(AbstractBaseUser, PermissionsMixin):
   """Modelo de usuario personalizado que usa email como campo de autenticación."""
   nombre=models.CharField(max_length=50, verbose_name="Nombre del usuario")
   apellido=models.CharField(max_length=50, verbose_name="Apellido del usuario")
   email=models.EmailField(unique=True, verbose_name="E-mail del usuario")

   is_active=models.BooleanField(default=True)
   is_staff=models.BooleanField(default=False)

   objects=CustomUserManager()

   USERNAME_FIELD='email'
   REQUIRED_FIELDS=['nombre','apellido']

 

   
   class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['email']


   def __str__(self):
       return self.email

