# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wedding', '0008_auto_20150708_1817'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlanText',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('template', models.TextField(null=True, blank=True)),
                ('slug', models.CharField(unique=True, max_length=16)),
                ('order', models.SmallIntegerField()),
            ],
        ),
    ]
