from django.conf.urls import url, include
from .views import *


urlpatterns = [
    url(r'^crear_usuario/$', CrearUsuario.as_view(), name="crear_usuario"),
    url(r'^listar_usuarios/$', listar_usuarios, name="listar_usuarios"),
    url(r'^modificar_usuario/(?P<id_usuario>\d+)$', ModificarUsuario.as_view(), name="modificar_usuario"),
    url(r'^eliminar_usuario/$', eliminar_usuario.as_view(), name="eliminar_usuario"),
    url(r'^activar_usuario/$', activar_usuario.as_view(), name="activar_usuario"),
    url(r'^ingresar', loginIn, name="iniciar_sesion"),
    url(r'^salir$', logout_view,  name="cerrar_sesion"),
    url(r'^error_403$', error_403,  name="error_403"),
    url(r'^coming_soon/$', coming_soon.as_view(),  name="coming_soon"),
]