# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wedding', '0007_invitation_sent_ts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='email1',
            field=models.EmailField(max_length=254, null=True, verbose_name=b'Primary Email', blank=True),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='email2',
            field=models.EmailField(max_length=254, null=True, verbose_name=b'Alternate Email', blank=True),
        ),
    ]