# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-20 17:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Facturacion', '0003_auto_20170719_1224'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factura',
            name='id',
        ),
        migrations.AlterField(
            model_name='factura',
            name='consecutivo',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='consecutivo'),
        ),
    ]