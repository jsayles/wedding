# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def set_tier(apps, schema_editor):
	Invitation = apps.get_model("wedding", "Invitation")
	for invite in Invitation.objects.all():
		invite.tier = '1'
		invite.save()

class Migration(migrations.Migration):

	dependencies = [
		('wedding', '0003_auto_20150122_1402'),
	]

	operations = [
		migrations.AddField(
			model_name='invitation',
			name='tier',
			field=models.CharField(default=b'4', max_length=1, verbose_name=b'Tier', choices=[(b'1', b'First'), (b'2', b'Second'), (b'3', b'Third'), (b'4', b'Fourth')]),
			preserve_default=True,
		),
		migrations.RunPython(set_tier),
	]
