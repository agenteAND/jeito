# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-07 07:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0014_auto_20170204_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='function',
            name='category',
            field=models.IntegerField(blank=True, choices=[(0, 'Jeune'), (1, 'Responsable'), (2, 'Cadre bénévole'), (3, 'Stagiaire'), (4, 'Parent/Ami'), (5, 'Salarié')], null=True, verbose_name='Categorie'),
        ),
        migrations.AlterField(
            model_name='rate',
            name='category',
            field=models.IntegerField(blank=True, choices=[(1, 'Enfant'), (2, 'Responsable'), (3, 'Soutien'), (4, 'Stagiaire'), (5, 'Import SV/CP'), (6, 'Découverte'), (7, 'Salarié')], null=True, verbose_name='Catégorie'),
        ),
    ]