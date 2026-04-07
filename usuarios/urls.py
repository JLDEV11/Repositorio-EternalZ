from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from . forms import CustomPasswordResetForm, CustomPasswordResetConfirmView

urlpatterns=[
    path("registrar_usuario",views.registrar_usuario, name="registrar_usuario"),
    path("iniciar_sesion",views.iniciar_sesion, name="iniciar_sesion"),
    path("cerrar_sesion", views.cerrar_sesion, name="cerrar_sesion"),
    path("cambiar_contrasena/", auth_views.PasswordResetView.as_view(form_class=CustomPasswordResetForm, template_name="usuarios/cambiar_contrasena.html"), name="reset_password"),
    path("cambiar_contrasena_enviado/", auth_views.PasswordResetDoneView.as_view(template_name="usuarios/contrasena_enviado.html"), name="password_reset_done"),
    path("nueva_contrasena/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(form_class=CustomPasswordResetConfirmView,template_name="usuarios/nueva_contrasena.html"), name="password_reset_confirm"),
    path("nueva_contrasena_completado/", auth_views.PasswordResetCompleteView.as_view(template_name="usuarios/contrasena_completado.html"), name="password_reset_complete"),
    
    
    
    


]