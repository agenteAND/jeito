# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-17 22:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='title',
            field=models.CharField(blank=True, max_length=100, verbose_name='Intitulé'),
        ),
    ]
