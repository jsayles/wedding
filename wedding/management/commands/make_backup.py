import os
import time
import urllib
import sys
import datetime

from django.core.management.base import BaseCommand, CommandError

from staff.backup import BackupManager

class Command(BaseCommand):
	help = "Creates a backup containing an SQL dump and the media files."
	args = ""
	requires_model_validation = False

	def handle(self, *labels, **options):
		manager = BackupManager()
		print manager.make_backup()

# Copyright 2011 Trevor F. Smith (http://trevor.smith.name/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
