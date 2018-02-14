from __future__ import unicode_literals
from django import forms
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import FilteredSelectMultiple

# Create your models here.

class Categoria(models.Model):
    
    tipo = models.CharField(max_length=200,verbose_name="tipo")        
    nombre = models.CharField(max_length=200,verbose_name="categoria")
    imagen = models.ImageField(null=True,blank=True,upload_to='img/categorias/',width_field="width_field",height_field = "height_field")
    height_field= models.IntegerField(default=0)
    width_field= models.IntegerField(default=0)
    disponible = models.BooleanField(default=True)
    
    class Meta:
		db_table = 'categoria'
		
class Producto(models.Model):
            
    referencia = models.CharField(primary_key=True,max_length=100,verbose_name="referencia")
    marca = models.CharField(max_length=100,verbose_name="marca")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=200,verbose_name="tipo", default="")
    tipo_contenido = models.CharField(max_length=200,verbose_name="tipo_contenido", default="Litros")
    grado_alimenticio = models.CharField(max_length=10,verbose_name="grado_alimenticio", default="No")
    pronostico_inicial = models.CharField(max_length=10,verbose_name="pronostico_inicial", default="30")
    disponibilidad = models.CharField(max_length=100,verbose_name="disponibilidad", default="Si")
    descripcion = models.CharField(max_length=100,verbose_name="descripcion", default="")
    imagen = models.ImageField(null=True,blank=True,upload_to='img/categorias/',width_field="width_field",height_field = "height_field", default='image_default.png')
    height_field= models.IntegerField(default=0)
    width_field= models.IntegerField(default=0) 
    
    
    #Fichas Obligatorias
    ficha_comercial = models.FileField(null=True,blank=True,upload_to='fichas-comerciales/')
    ficha_tecnica = models.FileField(null=True,blank=True,upload_to='fichas-tecnicas/')
    ficha_seguridad = models.FileField(null=True,blank=True,upload_to='fichas-seguridad/')
    
    
    #Fichas comerciales alternativas
    ficha_comercial_litografias = models.FileField(null=True,blank=True,upload_to='fichas-comerciales-litografias/')
    ficha_comercial_cementeras = models.FileField(null=True,blank=True,upload_to='fichas-comerciales-cementeras/')
    ficha_comercial_gruas = models.FileField(null=True,blank=True,upload_to='fichas-comerciales-gruas/')
    ficha_comercial_alimentaria = models.FileField(null=True,blank=True,upload_to='fichas-comerciales-alimentaria/')
    
    
    class Meta:
		db_table = 'producto'
		
		

class Presentacion(models.Model):
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    disponibilidad = models.CharField(max_length=100,verbose_name="disponibilidad")
    precio = models.IntegerField(verbose_name="precio")
    numero_elementos = models.IntegerField(verbose_name="numero_elementos")
    tipo_cantidad = models.CharField(max_length=100,verbose_name="tipo_cantidad")#KG, ML
    cantidad = models.CharField(max_length=100,verbose_name="cantidad")# Cuanto trae cada unidad
    empaque = models.CharField(max_length=100,verbose_name="empaque", default = "Aerosol")# Cuanto trae cada unidad
    unidades_en_stock = models.IntegerField(verbose_name="unidades_en_stock", default = 1000)
    disponible = models.BooleanField(default=True)
    
    class Meta:
		db_table = 'presentacion'
		
    def descripcion(self):
        return str(self.numero_elementos) + " " + str(self.empaque) + " " + str(self.cantidad) + " " + str(self.tipo_cantidad)
	
    
    
    
class Industria(models.Model):
    
    imagen = models.ImageField(null=True,blank=True,upload_to='img/categorias/')
    nombre = models.CharField(max_length=100,verbose_name="nombre")
    productos = models.ManyToManyField(Producto)    
    disponible = models.BooleanField(default=True)
    
    class Meta:
		db_table = 'industria'
    
