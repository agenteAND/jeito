# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-19 23:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_rate_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='rate',
            name='bracket',
            field=models.CharField(blank=True, max_length=100, verbose_name='Tranche'),
        ),
    ]
