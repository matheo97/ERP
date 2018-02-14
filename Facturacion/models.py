from __future__ import unicode_literals

from django.db import models
from Producto.models import Presentacion
from Cliente.models import Cliente
from django.contrib.auth.models import User
# Create your models here.


class Carrito(models.Model):
    
    presentaciones = models.ManyToManyField(Presentacion)
    encargado = models.ForeignKey(User,on_delete=models.CASCADE)
    cliente = models.CharField(max_length=100,verbose_name="cliente", default="")
    contacto = models.CharField(max_length=100,verbose_name="contacto", default="")
    
    class Meta:
		db_table = 'Carrito'
		
		
	
class PresentacionDeclarada(models.Model):
    
    cantidad = models.CharField(max_length=100,verbose_name="cantidad")
    precio_unidad = models.CharField(max_length=100,verbose_name="cantidad")
    precio_total = models.CharField(max_length=100,verbose_name="cantidad")
    presentacion = models.ForeignKey(Presentacion)
    
    class Meta:
		db_table = 'PresentacionDeclarada'
		
class Factura(models.Model):
    
    presentaciones = models.ManyToManyField(PresentacionDeclarada)
    encargado = models.CharField(max_length=100,verbose_name="encargado", default="")
    cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE)
    contacto = models.CharField(max_length=100,verbose_name="contacto", default="")
    consecutivo = models.CharField(primary_key=True, max_length=100,verbose_name="consecutivo")
    subtotal = models.CharField(max_length=100,verbose_name="subtotal", default="")
    tipo_pago = models.CharField(max_length=100,verbose_name="tipo_pago", default="")
    iva = models.CharField(max_length=100,verbose_name="iva", default="")
    total = models.CharField(max_length=100,verbose_name="total", default="")
    fecha = models.DateTimeField(auto_now_add=True)
    condicion_pago = models.CharField(max_length=100,verbose_name="codicion_pago", default="Inmediata")
    validez_oferta = models.CharField(max_length=100,verbose_name="validez_oferta", default="Inmediata")
    tiempo_entrega = models.CharField(max_length=100,verbose_name="tiempo_entrega", default="Inmediata")
    
    class Meta:
		db_table = 'Factura'
		
		
		
class Cotizacion(models.Model):
    
    presentaciones = models.ManyToManyField(PresentacionDeclarada)
    encargado = models.CharField(max_length=100,verbose_name="encargado", default="")
    cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE)
    contacto = models.CharField(max_length=100,verbose_name="contacto", default="")
    subtotal = models.CharField(max_length=100,verbose_name="subtotal", default="")
    iva = models.CharField(max_length=100,verbose_name="iva", default="")
    total = models.CharField(max_length=100,verbose_name="total", default="")
    condicion_pago = models.CharField(max_length=100,verbose_name="codicion_pago", default="Inmediata")
    validez_oferta = models.CharField(max_length=100,verbose_name="validez_oferta", default="Inmediata")
    tiempo_entrega = models.CharField(max_length=100,verbose_name="tiempo_entrega", default="Inmediata")
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
		db_table = 'Cotizacion'
		
		
		
class Remision(models.Model):
    
    presentaciones = models.ManyToManyField(PresentacionDeclarada)
    encargado = models.CharField(max_length=100,verbose_name="encargado", default="")
    cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE)
    contacto = models.CharField(max_length=100,verbose_name="contacto", default="")
    fecha = models.DateTimeField(auto_now_add=True)
    subtotal = models.CharField(max_length=100,verbose_name="subtotal", default="")
    iva = models.CharField(max_length=100,verbose_name="iva", default="")
    total = models.CharField(max_length=100,verbose_name="total", default="")
    condicion_pago = models.CharField(max_length=100,verbose_name="codicion_pago", default="Inmediata")
    validez_oferta = models.CharField(max_length=100,verbose_name="validez_oferta", default="Inmediata")
    tiempo_entrega = models.CharField(max_length=100,verbose_name="tiempo_entrega", default="Inmediata")
    
    class Meta:
		db_table = 'Remision'
		
		

