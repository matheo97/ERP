from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Cliente(models.Model):
    
    razon_social = models.CharField(max_length=100,verbose_name="razon social")
    nit = models.CharField(primary_key=True, max_length=100,verbose_name="nit")
    sigla = models.CharField(max_length=100,verbose_name="sigla")
    ciudad = models.CharField(max_length=100,verbose_name="ciudad")
    tipo = models.CharField(max_length=100,verbose_name="tipo", default="")
    departamento = models.CharField(max_length=100,verbose_name="departamento")
    direccion = models.CharField(max_length=100,verbose_name="direccion")
    telefono = models.CharField(max_length=100,verbose_name="telefono", null=True, default="")
    
    class Meta:
		db_table = 'cliente'
    
    
class Contacto(models.Model):
    
    nombre = models.CharField(max_length=100,verbose_name="nombre")
    correo_electronico = models.EmailField(verbose_name="correo electronico", null=True, default="")
    telefono = models.CharField(max_length=100,verbose_name="telefono", null=True, default="")
    extension = models.CharField(max_length=100,verbose_name="extension", null=True, default="")
    celular = models.CharField(max_length=100,verbose_name="celular", null=True, default="")
    cargo = models.CharField(max_length=100,verbose_name="cargo", null=True, default="")
    empresa = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    
    class Meta:
		db_table = 'contacto'