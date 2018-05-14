# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-14 08:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0006_userinfo_age'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='age',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='email',
            field=models.EmailField(default='112@qq.com', max_length=254, unique=True, verbose_name='邮箱'),
            preserve_default=False,
        ),
    ]
