from django.conf.urls import url, include
from django.contrib import admin
import settings
from LandingPage.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home, name="home"),
    url(r'^about-us/$', about_us, name="about-us"),
    url(r'^videos/$', videos, name="videos"),
    url(r'^contact-us/$', contact_us.as_view(), name="contact-us"),
    url(r'^email_contactenos/$', email_contactenos, name="email_contactenos"),
    url(r'^portafolio/(?P<id_tipo>\d+)$', portafolio, name="portafolio"),
    url(r'^producto_grado_alimenticio/(?P<id_tipo>\d+)$', resultado_productos, name="producto_grado_alimenticio"),
    url(r'^productos_categoria/(?P<id_categoria>\d+)$', productos_categoria, name="productos_categoria"),
    url(r'^productos_industria/(?P<id_industria>\d+)$', productos_industria, name="productos_industria"),
    url(r'^industria/$', industria, name="industria"),
    url(r'^productos_grado_alimenticio/$', mostrar_grado_alimenticio, name="mostrar_grado_alimenticio"),
    url(r'^cliente/', include('Cliente.urls', namespace='cliente')),
    url(r'^producto/', include('Producto.urls', namespace='producto')),
    url(r'^usuario/', include('Usuario.urls', namespace='usuario')),
    url(r'^facturacion/', include('Facturacion.urls', namespace='facturacion')),
    url(r'^demanda/', include('Demanda.urls', namespace='demanda')),
]