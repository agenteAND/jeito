# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-05 12:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0017_auto_20170305_1358'),
    ]

    operations = [
        migrations.RunSQL('''INSERT INTO members_nomination(adhesion_id, structure_id, function_id, main)
                             SELECT id, structure_id, function_id, TRUE FROM members_adhesion;'''),
    ]
