# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-28 17:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_comment_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='time_edited',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
