# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-10-05 04:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('members', '0021_person_birthdate'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('function', models.TextField(blank=True, max_length=100)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('location', models.CharField(blank=True, max_length=100, verbose_name='Lieu')),
                ('nb_presents', models.IntegerField(blank=True, null=True, verbose_name='Nombre de personnes présentes')),
                ('nb_voters', models.IntegerField(blank=True, null=True, verbose_name='Nombre de votants')),
                ('favour', models.PositiveIntegerField(blank=True, null=True, verbose_name='Pour')),
                ('against', models.PositiveIntegerField(blank=True, null=True, verbose_name='Contre')),
                ('abstention', models.PositiveIntegerField(blank=True, null=True, verbose_name='Abstention')),
                ('balance', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, verbose_name='Résultat exercice en cours')),
                ('budget', models.NullBooleanField(verbose_name="Présentation d'un budget prévisionnel")),
                ('responsible_validation', models.NullBooleanField(verbose_name='Signature du responsable de la SLA')),
                ('representative_validation', models.NullBooleanField(verbose_name='Signature du représentant')),
                ('comments_activity_report', models.TextField(blank=True, verbose_name="Commentaires concernant le temps rapport d'activité")),
                ('comments_finances', models.TextField(blank=True, verbose_name='Commentaires concernant le point financier')),
                ('comments_national', models.TextField(blank=True, verbose_name="Commentaires concernant les sujets d'intérêts nationaux abordés")),
                ('comments_regional', models.TextField(blank=True, verbose_name="Commentaires concernant les sujets d'intérêts régionaux abordés")),
                ('comments_problems', models.TextField(blank=True, verbose_name='Problèmes/difficultés survenus dans la tenue de la réunion')),
                ('alternate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='report_alternate_set', to=settings.AUTH_USER_MODEL, verbose_name='Délégué suppléant élu')),
                ('delegate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='report_delegate_set', to=settings.AUTH_USER_MODEL, verbose_name='Délégué élu')),
                ('representative', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='report_representative_set', to=settings.AUTH_USER_MODEL, verbose_name='Représentant')),
                ('responsible', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='report_responsible_set', to=settings.AUTH_USER_MODEL, verbose_name='Responsable')),
                ('structure', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='members.Structure', verbose_name='SLA')),
                ('team', models.ManyToManyField(through='life.Membership', to=settings.AUTH_USER_MODEL)),
                ('treasurer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='report_treasurer_set', to=settings.AUTH_USER_MODEL, verbose_name='Trésorier')),
            ],
        ),
        migrations.AddField(
            model_name='membership',
            name='report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='life.Report'),
        ),
    ]
