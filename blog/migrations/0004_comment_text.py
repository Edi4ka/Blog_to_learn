# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-28 16:24
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20160228_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='text',
            field=models.TextField(default=datetime.datetime(2016, 2, 28, 16, 24, 21, 878524, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
