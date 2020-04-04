# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2020-04-03 09:12
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20200403_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
        migrations.AlterField(
            model_name='post',
            name='pubdate',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 3, 9, 12, 45, 879210, tzinfo=utc), verbose_name='创建时间'),
        ),
    ]
