# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wedding', '0004_invitation_tier'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuestNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('from_name', models.CharField(max_length=64, verbose_name=b'From')),
                ('note', models.TextField()),
                ('approved', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
