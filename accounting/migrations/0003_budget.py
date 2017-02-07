# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-07 18:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0002_auto_20170207_1411'),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Montant')),
                ('analytic', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounting.Analytic', verbose_name='Analytique')),
            ],
        ),
    ]