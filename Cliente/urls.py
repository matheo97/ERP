from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^crear_cliente/$', CrearCliente.as_view(), name="crear_cliente"),
    url(r'^crear_contacto/(?P<id_cliente>.+)$', CrearContacto.as_view(), name="crear_contacto"),
    url(r'^listar_clientes/$', listar_clientes.as_view(), name="listar_clientes"),
    url(r'^listar_contactos/(?P<id_cliente>.+)$', listar_contactos, name="listar_contactos"),
    url(r'^visualizar_cliente/(?P<id_cliente>.+)$', visualizar_cliente, name="visualizar_cliente"),
    url(r'^modificar_cliente/(?P<id_cliente>.+)$', ModificarCliente.as_view(), name="modificar_cliente"),
    url(r'^modificar_contacto/(?P<id_contacto>\d+)$', ModificarContacto.as_view(), name="modificar_contacto"),
    url(r'^buscar_cliente/$', buscar_cliente.as_view(), name="buscar_cliente"),
    url(r'^carrito_contacto/(?P<id_contacto>\d+)$', carrito_contacto, name="carrito_contacto"),
]