# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wedding', '0006_auto_20150215_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='sent_ts',
            field=models.DateTimeField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
    ]
