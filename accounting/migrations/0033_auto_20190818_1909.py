# Generated by Django 2.1.7 on 2019-08-18 17:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0032_auto_20190818_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thirdparty',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounting.Account', verbose_name='Compte principal'),
        ),
    ]