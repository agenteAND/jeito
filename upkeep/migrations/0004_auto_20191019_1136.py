# Generated by Django 2.2.6 on 2019-10-19 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upkeep', '0003_issue_blocks'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='issue',
            options={'verbose_name': 'Problème'},
        ),
        migrations.AlterModelOptions(
            name='place',
            options={'verbose_name': 'Emplacement'},
        ),
        migrations.AlterModelOptions(
            name='skill',
            options={'verbose_name': 'Compétence'},
        ),
    ]
