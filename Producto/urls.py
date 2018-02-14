from django.conf.urls import url, include
from .views import *


urlpatterns = [
    url(r'^crear_categoria/$', CrearCategoria.as_view(), name="crear_categoria"),
    url(r'^listar_categorias/$', ListarCategoria.as_view(), name="listar_categorias"),
    url(r'^modificar_categoria/(?P<id_categoria>\d+)$', ModificarCategoria.as_view(), name="modificar_categoria"),
    url(r'^desactivar_categoria/$', desactivar_categoria.as_view(), name="desactivar_categoria"),
    url(r'^activar_categoria/$', activar_categoria.as_view(), name="activar_categoria"),
    url(r'^crear_producto/$', CrearProducto.as_view(), name="crear_producto"),
    url(r'^crear_producto/cargar_categoria/$', CargarCategorias.as_view(), name="cargar_categoria"),
    url(r'^listar_productos/cargar_categoria/$', CargarCategorias.as_view(), name="cargar_categoria2"),
    url(r'^listar_productos/$', ListarProductos.as_view(), name="listar_productos"),
    url(r'^activar_productos/(?P<referencia_producto>\w+)$', activar_producto, name="activar_producto"),
    url(r'^modificar_producto/(?P<id_producto>\w+)$', ModificarProducto.as_view(), name="modificar_producto"),
    url(r'^eliminar_producto/$', eliminar_producto.as_view(), name="eliminar_producto"),
    url(r'^crear_presentaciones/(?P<referencia_producto>\w+)$', CrearPresentacion.as_view(), name="crear_presentacion"),
    url(r'^listar_presentaciones/(?P<referencia_producto>\w+)$', listar_presentaciones, name="listar_presentaciones"),
    url(r'^modificar_presentacion/(?P<id_presentacion>\d+)$', ModificarPresentacion.as_view(), name="modificar_presentacion"),
    url(r'^eliminar_presentacion/$', eliminar_presentacion.as_view(), name="eliminar_presentacion"),
    url(r'^activar_presentacion/$', activar_presentacion.as_view(), name="activar_presentacion"),
    url(r'^carrito_presentacion/(?P<id_presentacion>\d+)$', carrito_presentacion, name="carrito_presentacion"),
    url(r'^crear_industria/$', crearIndustria.as_view(), name="crear_industria"),
    url(r'^listar_industrias/$', listarIndustria.as_view(), name="listar_industrias"),
    url(r'eliminar_industria/$', eliminar_industria.as_view(), name="eliminar_industria"),
    url(r'activar_industria/$', activar_industria.as_view(), name="activar_industria"),
    url(r'^modificar_industria/(?P<id_industria>\d+)$', ModificarIndustria.as_view(), name="modificar_industria"),
    url(r'eliminar_producto_industria/(?P<id_industria>\d+)$', eliminar_producto_industria.as_view(), name="eliminar_producto_industria"),
    url(r'^filtrar_categorias/$', filtrar_categorias, name="filtrar_categorias"),
    url(r'^filtrar_productos/$', filtrar_productos, name="filtrar_productos"),
    url(r'^filtrar_industrias/$', filtrar_industrias, name="filtrar_industrias"),
    url(r'^generar_presentaciones_automaticas/$', generar_presentaciones_automaticas, name="generar_presentaciones_automaticas"),
]