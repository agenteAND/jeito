# Generated by Django 2.1.7 on 2019-09-02 22:09

from django.db import migrations


def set_type(apps, schema_editor):
    ThirdParty = apps.get_model('accounting', 'ThirdParty')
    ThirdParty.objects.filter(account__number='4010000').update(type=1)
    ThirdParty.objects.filter(account__number='4090000').update(type=1)
    ThirdParty.objects.filter(account__number='4670000').update(type=3)


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0036_thirdparty_type'),
    ]

    operations = [
        migrations.RunPython(set_type, migrations.RunPython.noop),
    ]
