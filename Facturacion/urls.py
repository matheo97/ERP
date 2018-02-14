from django.conf.urls import url, include
from .views import *

urlpatterns = [
     
     url(r'^generar_cotizacion/$', generarCotizacion.as_view(), name="generar_cotizacion"),
     url(r'^generar_factura/$', generarFactura.as_view(), name="generar_factura"),
     url(r'^editar_factura/(?P<id_factura>\w+)$', editarFactura.as_view(), name="editar_factura"),
     url(r'^generar_factura_cotizacion/(?P<id_cotizacion>\d+)$', generarFacturadeCotizacion.as_view(), name="generar_factura_cotizacion"),
     url(r'^generar_remision/$', generarRemision.as_view(), name="generar_remision"),
     url(r'^generar_cotizacion/eliminar_presentacion_carrito$', eliminarPresentacionCarrito.as_view(), name="eliminar_presentacion_carrito"),
     url(r'^generar_factura/eliminar_presentacion_carrito$', eliminarPresentacionCarrito.as_view(), name="eliminar_presentacion_carrito"),
     url(r'^listar_facturacion/(?P<id_cliente>.+)$', listarFacturacion.as_view(), name="listar_facturacion"),
     url(r'^listar_facturas/(?P<id_cliente>.+)$', listar_facturas, name="listar_facturas"),
     url(r'^listar_cotizaciones/(?P<id_cliente>.+)$', listar_cotizaciones, name="listar_cotizaciones"),
     url(r'^listar_remisiones/(?P<id_cliente>.+)$', listar_remisiones, name="listar_remisiones"),
     url(r'^generar_cotizacion_pdf/(?P<id_cotizacion>\d+)$', generarCotizacionPDF.as_view(), name="generarCotizacion_pdf"),
     url(r'^generar_factura_pdf/(?P<id_factura>\w+)$', generarFacturaPDF.as_view(), name="generarFactura_pdf"),
     url(r'^generar_factura/validar_consecutivo/', validar_consecutivo, name="validar_consecutivo"),
     url(r'^generar_factura_cotizacion/validar_consecutivo/', validar_consecutivo, name="generar_factura_cotizacion_1"),
     url(r'^generar_remision_pdf/(?P<id_remision>\d+)$', generarRemisionPDF.as_view(), name="generarRemision_pdf"),
     url(r'^ver_factura/(?P<id_factura>\d+)$', verFactura.as_view(), name="ver_factura"),
     url(r'^limpiar_carrito/(?P<documento>\w+)$', limpiar_carrito, name="limpiar_carrito"),
     url(r'^eliminar_factura/$', eliminar_factura.as_view(), name="eliminar_factura"),
]