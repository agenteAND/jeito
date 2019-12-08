# Generated by Django 2.2.8 on 2019-12-08 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0055_auto_20191102_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenditure',
            name='method',
            field=models.IntegerField(choices=[(1, 'Carte bancaire'), (2, 'Chèque'), (3, 'Espèces'), (4, "Prélèvement"), (5, 'Virement')], default=0),
            preserve_default=False,
        ),
    ]
