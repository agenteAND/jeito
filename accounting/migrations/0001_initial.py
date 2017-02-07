# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-07 07:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=7, verbose_name='Numéro')),
                ('title', models.CharField(max_length=100, verbose_name='Intitulé')),
            ],
            options={
                'verbose_name': 'Compte',
            },
        ),
        migrations.CreateModel(
            name='Analytic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Intitulé')),
            ],
            options={
                'verbose_name': 'Compte',
            },
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date')),
                ('title', models.CharField(max_length=100, verbose_name='Intitulé')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Montant')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.Account', verbose_name='Compte')),
                ('analytic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounting.Analytic', verbose_name='Analytique')),
            ],
            options={
                'verbose_name': 'Écriture',
            },
        ),
    ]
