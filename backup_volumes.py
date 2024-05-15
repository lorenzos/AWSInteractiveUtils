# -*- coding: utf-8 -*-

### INTERACTIVELY BACKUPS EC2 VOLUMES CREATING SNAPSHOTS
### If an instance has tag NoBackup=1, then it's not listed and not backupped

### CONFIGURATION
REGION = 'eu-west-1'
PROFILE_NAME = 'VolumeBackupper'

###

import os
import re
import time
from datetime import datetime
from boto import ec2
from colorama import Fore, Back, Style

exec(compile(open(os.path.abspath(os.path.dirname(__file__)) + '/commons.py', "rb").read(), os.path.abspath(os.path.dirname(__file__)) + '/commons.py', 'exec'))
printTitle('EC2 VOLUME BACKUP', 'Backups volumes creating snapshots, excluding volumes with tag NoBackup=1')
print() 

connection = ec2.connect_to_region(REGION, profile_name = PROFILE_NAME)

# Ask which volumes to backup and their snapshot description
backups = []
for volume in connection.get_all_volumes():
	if volume.tags.get('NoBackup', '0') != '1':
		volume_name = volume.tags.get('Name', '(no name)')
		if questionYN('Do you want to backup volume ' + Style.BRIGHT + '{}' + Style.NORMAL + ' ({})', volume_name, volume.id):
			description = questionInput(Fore.BLUE + ' -> Insert snapshot description for ' + Style.BRIGHT + '{}' + Style.RESET_ALL, volume_name)
			backups.append({ 'volume': volume, 'volume_name': volume_name, 'description': description, 'volume_tags': volume.tags })

if len(backups) > 0:
	
	print()
	
	# Create snapshots
	snapshots_ids = []
	snapshot_name_re = re.compile(' ?volume ?', re.IGNORECASE)
	snapshot_name_suffix = ' @{:%Y-%m-%d}'.format(datetime.now())
	for backup in backups:
		snapshot = backup['volume'].create_snapshot(backup['description'] if backup['description'] != 0 else None)
		snapshot_name = snapshot_name_re.sub(' ', backup['volume_name']).strip() + snapshot_name_suffix
		snapshot_tags = backup['volume_tags'] # Inherit tags from volume...
		snapshot_tags['Name'] = snapshot_name # ...but customize the name tag
		connection.create_tags(snapshot.id, snapshot_tags)
		print(Fore.GREEN + 'Creating snapshot ' + Style.BRIGHT + snapshot_name + Style.NORMAL + ' (' + snapshot.id + ') with size ' + str(snapshot.volume_size) + 'GB...' + Style.RESET_ALL)
		snapshots_ids.append(snapshot.id)
	
	print()
	
	# Check progress every 5 seconds
	end = False
	while not end:
		time.sleep(5)
		end = True
		for snapshot in connection.get_all_snapshots(snapshot_ids = snapshots_ids, owner = 'self'):
			completed = snapshot.status == 'completed' and snapshot.progress.rstrip('%') == '100'
			print((Fore.GREEN if completed else Fore.YELLOW) + 'Snapshot ' + Style.BRIGHT + snapshot.tags.get('Name', '(no name)') + Style.NORMAL + ' ' + snapshot.status + ' (' + (snapshot.progress.rstrip('%') or '0')  + '%)...' + Style.RESET_ALL)
			end = end and completed
		print()
	
	print(Fore.GREEN + Style.BRIGHT + 'All snapshop created and completed.' + Style.RESET_ALL, end=' ')
	input()

