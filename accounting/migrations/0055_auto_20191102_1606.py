# Generated by Django 2.2.6 on 2019-11-02 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0054_auto_20191031_0609'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='purchase',
            options={'verbose_name': 'Facture fournisseur', 'verbose_name_plural': 'Factures fournisseur'},
        ),
        migrations.AlterModelOptions(
            name='sale',
            options={'verbose_name': 'Facture client', 'verbose_name_plural': 'Factures client'},
        ),
    ]
