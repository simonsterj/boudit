# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-06-10 09:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0002_shawtyurl_shortcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shawtyurl',
            name='shortcode',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]