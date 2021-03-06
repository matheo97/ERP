# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-05 19:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=200, verbose_name='tipo')),
                ('nombre', models.CharField(max_length=200, verbose_name='categoria')),
                ('imagen', models.ImageField(blank=True, height_field='height_field', null=True, upload_to='img/categorias/', width_field='width_field')),
                ('height_field', models.IntegerField(default=0)),
                ('width_field', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'categoria',
            },
        ),
        migrations.CreateModel(
            name='Presentacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disponibilidad', models.CharField(max_length=100, verbose_name='disponibilidad')),
                ('precio', models.IntegerField(verbose_name='precio')),
                ('numero_elementos', models.IntegerField(verbose_name='numero_elementos')),
                ('tipo_cantidad', models.CharField(max_length=100, verbose_name='tipo_cantidad')),
                ('cantidad', models.CharField(max_length=100, verbose_name='cantidad')),
            ],
            options={
                'db_table': 'presentacion',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('referencia', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='referencia')),
                ('marca', models.CharField(max_length=100, verbose_name='marca')),
                ('tipo', models.CharField(default='', max_length=200, verbose_name='tipo')),
                ('ficha_comercial', models.FileField(blank=True, null=True, upload_to='fichas-comerciales/')),
                ('ficha_tecnica', models.FileField(blank=True, null=True, upload_to='fichas-tecnicas/')),
                ('ficha_seguridad', models.FileField(blank=True, null=True, upload_to='fichas-seguridad/')),
                ('disponibilidad', models.CharField(max_length=100, verbose_name='disponibilidad')),
                ('descripcion', models.CharField(default='', max_length=1000, verbose_name='descripcion')),
                ('imagen', models.ImageField(blank=True, height_field='height_field', null=True, upload_to='img/categorias/', width_field='width_field')),
                ('height_field', models.IntegerField(default=0)),
                ('width_field', models.IntegerField(default=0)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Producto.Categoria')),
            ],
            options={
                'db_table': 'producto',
            },
        ),
        migrations.AddField(
            model_name='presentacion',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Producto.Producto'),
        ),
    ]
