from __future__ import unicode_literals

from django.db import models
from Producto.models import *

		
class Producto_Importacion(models.Model):
    
    tipo_contenido = models.CharField(max_length=100,verbose_name="tipo_contenido", null=True, default="")
    pronostico = models.CharField(max_length=100,verbose_name="pronostico", null=True, default="0")
    cantidad = models.CharField(max_length=100,verbose_name="cantidad", null=True, default="0")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    pronostico_total = models.CharField(max_length=20,verbose_name="total_pronostico", default="0")
    
    class Meta:
		db_table = 'producto_importacion'
		
		
class Listado_Productos(models.Model):
    
    referencia_periodo = models.CharField(max_length=100,verbose_name="referencia_periodo")
    productos = models.ManyToManyField(Producto_Importacion)
    
    class Meta:
		db_table = 'listado_productos'
		
		
class Aplicacion_Futura(models.Model):
    
    probabilidad = models.CharField(max_length=100,verbose_name="tipo_contenido", null=True, default="")
    pronostico_individual = models.CharField(max_length=100,verbose_name="tipo_contenido", null=True, default="")
    contacto = models.CharField(max_length=100,verbose_name="tipo_contenido", null=True, default="")
    cliente = models.CharField(max_length=100,verbose_name="tipo_contenido", null=True, default="")
    
    class Meta:
		db_table = 'Listado_Productos_Aplicacion_Futura'		
		
class Producto_Aplicacion_Futura(models.Model):
    
    referencia_periodo = models.CharField(max_length=100,verbose_name="referencia_periodo", null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    predicciones = models.ManyToManyField(Aplicacion_Futura)
    pronostico_total = models.CharField(max_length=100,verbose_name="tipo_contenido", null=True, default="")
    
    class Meta:
		db_table = 'producto_aplicacion_futura'
		
