from django.conf.urls import url, include
from .views import *

urlpatterns = [

    url(r'^crear_periodo_inicial/$', crear_periodo_inicial, name="crear_periodo_inicial"),
    url(r'^crear_aplicacion_futura/$', generarAplicacionFutura.as_view(), name="crear_aplicacion_futura"),
    url(r'^mostrar_prediccion/$', mostrarPrediccion.as_view(), name="mostrar_prediccion"),
    url(r'^eliminar_pronostico_individual/$', eliminar_pronostico_individual.as_view(), name="eliminar_pronostico_individual"),
]