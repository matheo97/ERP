# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-26 15:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Producto', '0010_remove_producto_tipo_contenido'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='pronostico_inicial',
            field=models.CharField(default='30', max_length=10, verbose_name='pronostico_inicial'),
        ),
    ]