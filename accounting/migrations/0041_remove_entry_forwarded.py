# Generated by Django 2.1.7 on 2019-10-06 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0040_remove_entry_projected'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='forwarded',
        ),
    ]
