# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-15 23:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eyeDetectServer', '0004_auto_20170515_1645'),
    ]

    operations = [
        migrations.RenameField(
            model_name='record',
            old_name='user_id',
            new_name='time',
        ),
    ]
