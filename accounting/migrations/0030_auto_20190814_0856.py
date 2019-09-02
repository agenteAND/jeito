# Generated by Django 2.1.7 on 2019-08-14 06:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0029_auto_20190814_0843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='journal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounting.Journal', verbose_name='Journal'),
        ),
    ]