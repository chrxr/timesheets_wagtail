# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-04 20:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20160704_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workday',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Project'),
        ),
    ]
