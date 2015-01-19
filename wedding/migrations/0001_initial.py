# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recipient', models.CharField(max_length=64, verbose_name=b'Recipient')),
                ('address_line1', models.CharField(max_length=64, verbose_name=b'Address line 1', blank=True)),
                ('address_line2', models.CharField(max_length=64, verbose_name=b'Address line 2', blank=True)),
                ('city', models.CharField(max_length=64, verbose_name=b'City', blank=True)),
                ('state', models.CharField(blank=True, max_length=2, verbose_name=b'State', choices=[(b'AL', b'Alabama'), (b'AK', b'Alaska'), (b'AS', b'American Samoa'), (b'AZ', b'Arizona'), (b'AR', b'Arkansas'), (b'AA', b'Armed Forces Americas'), (b'AE', b'Armed Forces Europe'), (b'AP', b'Armed Forces Pacific'), (b'CA', b'California'), (b'CO', b'Colorado'), (b'CT', b'Connecticut'), (b'DE', b'Delaware'), (b'DC', b'District of Columbia'), (b'FL', b'Florida'), (b'GA', b'Georgia'), (b'GU', b'Guam'), (b'HI', b'Hawaii'), (b'ID', b'Idaho'), (b'IL', b'Illinois'), (b'IN', b'Indiana'), (b'IA', b'Iowa'), (b'KS', b'Kansas'), (b'KY', b'Kentucky'), (b'LA', b'Louisiana'), (b'ME', b'Maine'), (b'MD', b'Maryland'), (b'MA', b'Massachusetts'), (b'MI', b'Michigan'), (b'MN', b'Minnesota'), (b'MS', b'Mississippi'), (b'MO', b'Missouri'), (b'MT', b'Montana'), (b'NE', b'Nebraska'), (b'NV', b'Nevada'), (b'NH', b'New Hampshire'), (b'NJ', b'New Jersey'), (b'NM', b'New Mexico'), (b'NY', b'New York'), (b'NC', b'North Carolina'), (b'ND', b'North Dakota'), (b'MP', b'Northern Mariana Islands'), (b'OH', b'Ohio'), (b'OK', b'Oklahoma'), (b'OR', b'Oregon'), (b'PA', b'Pennsylvania'), (b'PR', b'Puerto Rico'), (b'RI', b'Rhode Island'), (b'SC', b'South Carolina'), (b'SD', b'South Dakota'), (b'TN', b'Tennessee'), (b'TX', b'Texas'), (b'UT', b'Utah'), (b'VT', b'Vermont'), (b'VI', b'Virgin Islands'), (b'VA', b'Virginia'), (b'WA', b'Washington'), (b'WV', b'West Virginia'), (b'WI', b'Wisconsin'), (b'WY', b'Wyoming')])),
                ('zip_code', models.CharField(max_length=10, verbose_name=b'Zip Code', blank=True)),
                ('email1', models.EmailField(max_length=75, null=True, verbose_name=b'Primary Email', blank=True)),
                ('email2', models.EmailField(max_length=75, null=True, verbose_name=b'Alternate Email', blank=True)),
                ('rsvp_ceremony', models.PositiveSmallIntegerField(null=True, verbose_name=b'Confirmed Ceremony', blank=True)),
                ('rsvp_reception', models.PositiveSmallIntegerField(null=True, verbose_name=b'Confirmed Reception', blank=True)),
                ('rsvp_wv', models.PositiveSmallIntegerField(null=True, verbose_name=b'Confirmed West Virginia Reception', blank=True)),
                ('estimated_ceremony', models.PositiveSmallIntegerField(default=0, verbose_name=b'Estimated Ceremony')),
                ('estimated_reception', models.PositiveSmallIntegerField(default=0, verbose_name=b'Estimated Reception')),
                ('estimated_wv', models.PositiveSmallIntegerField(default=0, verbose_name=b'Estimated West Virginia Reception')),
                ('gift', models.CharField(max_length=64, verbose_name=b'Gift', blank=True)),
                ('thank_you_sent', models.BooleanField(default=False)),
                ('notes', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InvitationGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='invitation',
            name='groups',
            field=models.ManyToManyField(to='wedding.InvitationGroup', blank=True),
            preserve_default=True,
        ),
    ]
