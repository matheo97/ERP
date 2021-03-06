# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-11 01:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Producto', '0001_initial'),
        ('Facturacion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PresentacionDeclarada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.CharField(max_length=100, verbose_name='cantidad')),
                ('precio_unidad', models.CharField(max_length=100, verbose_name='cantidad')),
                ('precio_total', models.CharField(max_length=100, verbose_name='cantidad')),
                ('presentacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Producto.Presentacion')),
            ],
            options={
                'db_table': 'PresentacionDeclarada',
            },
        ),
        migrations.AlterField(
            model_name='cotizacion',
            name='presentaciones',
            field=models.ManyToManyField(to='Facturacion.PresentacionDeclarada'),
        ),
        migrations.AlterField(
            model_name='factura',
            name='presentaciones',
            field=models.ManyToManyField(to='Facturacion.PresentacionDeclarada'),
        ),
        migrations.AlterField(
            model_name='remision',
            name='presentaciones',
            field=models.ManyToManyField(to='Facturacion.PresentacionDeclarada'),
        ),
    ]
