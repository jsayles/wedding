# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wedding', '0005_guestnote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='address_line1',
            field=models.CharField(max_length=64, null=True, verbose_name=b'Address line 1', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invitation',
            name='address_line2',
            field=models.CharField(max_length=64, null=True, verbose_name=b'Address line 2', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invitation',
            name='city',
            field=models.CharField(max_length=64, null=True, verbose_name=b'City', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invitation',
            name='state',
            field=models.CharField(blank=True, max_length=2, null=True, verbose_name=b'State', choices=[(b'AL', b'Alabama'), (b'AK', b'Alaska'), (b'AS', b'American Samoa'), (b'AZ', b'Arizona'), (b'AR', b'Arkansas'), (b'AA', b'Armed Forces Americas'), (b'AE', b'Armed Forces Europe'), (b'AP', b'Armed Forces Pacific'), (b'CA', b'California'), (b'CO', b'Colorado'), (b'CT', b'Connecticut'), (b'DE', b'Delaware'), (b'DC', b'District of Columbia'), (b'FL', b'Florida'), (b'GA', b'Georgia'), (b'GU', b'Guam'), (b'HI', b'Hawaii'), (b'ID', b'Idaho'), (b'IL', b'Illinois'), (b'IN', b'Indiana'), (b'IA', b'Iowa'), (b'KS', b'Kansas'), (b'KY', b'Kentucky'), (b'LA', b'Louisiana'), (b'ME', b'Maine'), (b'MD', b'Maryland'), (b'MA', b'Massachusetts'), (b'MI', b'Michigan'), (b'MN', b'Minnesota'), (b'MS', b'Mississippi'), (b'MO', b'Missouri'), (b'MT', b'Montana'), (b'NE', b'Nebraska'), (b'NV', b'Nevada'), (b'NH', b'New Hampshire'), (b'NJ', b'New Jersey'), (b'NM', b'New Mexico'), (b'NY', b'New York'), (b'NC', b'North Carolina'), (b'ND', b'North Dakota'), (b'MP', b'Northern Mariana Islands'), (b'OH', b'Ohio'), (b'OK', b'Oklahoma'), (b'OR', b'Oregon'), (b'PA', b'Pennsylvania'), (b'PR', b'Puerto Rico'), (b'RI', b'Rhode Island'), (b'SC', b'South Carolina'), (b'SD', b'South Dakota'), (b'TN', b'Tennessee'), (b'TX', b'Texas'), (b'UT', b'Utah'), (b'VT', b'Vermont'), (b'VI', b'Virgin Islands'), (b'VA', b'Virginia'), (b'WA', b'Washington'), (b'WV', b'West Virginia'), (b'WI', b'Wisconsin'), (b'WY', b'Wyoming')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invitation',
            name='zip_code',
            field=models.CharField(max_length=10, null=True, verbose_name=b'Zip Code', blank=True),
            preserve_default=True,
        ),
    ]
