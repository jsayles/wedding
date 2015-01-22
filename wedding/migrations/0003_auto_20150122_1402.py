# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wedding', '0002_invitation_last_viewed'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='check_spelling',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invitation',
            name='mail_invitation',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
