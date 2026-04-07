from django.shortcuts import render, redirect
from .forms import CrearUsuarioForm, IniciarSesionForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required


# Create your views here.
@never_cache
def registrar_usuario(request):
    """Vista de registro de nuevo usuario. Crea cuenta y autentica automáticamente."""
    if request.user.is_authenticated:
        return redirect('index')
   
    if request.method=="POST":
        form=CrearUsuarioForm(request.POST)
        

        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect("index")


    else:
            form=CrearUsuarioForm()

    return render(request,"usuarios/registrar_usuario.html",{
        "form":form
    })
  
@never_cache
def iniciar_sesion(request):
    """Vista de inicio de sesión. Autentica al usuario con email y contraseña."""
    
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        form = IniciarSesionForm(request, data=request.POST)
        
        if form.is_valid():
            user = form.get_user()  
            login(request, user)
            return redirect("index")
     
        else:
            
            messages.error(request, "Email o contraseña incorrectos")
    else:
        form = IniciarSesionForm()

    return render(request, "usuarios/iniciar_sesion.html", {
        "form": form,
    })




@login_required
def cerrar_sesion(request):
     """Vista para cerrar sesión del usuario autenticado."""
     logout(request)
     return redirect("index")
 
 
 
