# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-12-05 01:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Producto', '0012_producto_tipo_contenido'),
        ('Demanda', '0006_producto_importacion_aplicaciones_futuras'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto_Aplicacion_Futura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pronostico_total', models.CharField(default='', max_length=100, null=True, verbose_name='tipo_contenido')),
            ],
            options={
                'db_table': 'producto_aplicacion_futura',
            },
        ),
        migrations.RemoveField(
            model_name='aplicacion_futura',
            name='cantidad',
        ),
        migrations.RemoveField(
            model_name='aplicacion_futura',
            name='mes_aplicacion',
        ),
        migrations.RemoveField(
            model_name='aplicacion_futura',
            name='presentacion',
        ),
        migrations.RemoveField(
            model_name='producto_importacion',
            name='aplicaciones_futuras',
        ),
        migrations.RemoveField(
            model_name='producto_importacion',
            name='aplicaciones_futuras_total',
        ),
        migrations.AddField(
            model_name='aplicacion_futura',
            name='cliente',
            field=models.CharField(default='', max_length=100, null=True, verbose_name='tipo_contenido'),
        ),
        migrations.AddField(
            model_name='aplicacion_futura',
            name='contacto',
            field=models.CharField(default='', max_length=100, null=True, verbose_name='tipo_contenido'),
        ),
        migrations.AddField(
            model_name='aplicacion_futura',
            name='pronostico_individual',
            field=models.CharField(default='', max_length=100, null=True, verbose_name='tipo_contenido'),
        ),
        migrations.AlterField(
            model_name='aplicacion_futura',
            name='probabilidad',
            field=models.CharField(default='', max_length=100, null=True, verbose_name='tipo_contenido'),
        ),
        migrations.AlterModelTable(
            name='aplicacion_futura',
            table='Listado_Productos_Aplicacion_Futura',
        ),
        migrations.AddField(
            model_name='producto_aplicacion_futura',
            name='predicciones',
            field=models.ManyToManyField(to='Demanda.Aplicacion_Futura'),
        ),
        migrations.AddField(
            model_name='producto_aplicacion_futura',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Producto.Producto'),
        ),
    ]