# -*- coding: utf-8 -*-

### CONNECTS TO ALL EC2 INSTANCES VIA SSH AND CHECKS THE DATE-TIME OFFSET

### CONFIGURATION
REGION = 'eu-west-1'
PROFILE_NAME = 'InstanceLister'
TERMINAL = 'xfce4-terminal -H'
SSH_CERTIFICATE = ['/home/lorenzo/.certificates/david-1.pem', '/home/lorenzo/.certificates/david-1-pocket-sell-app.pem']
CHECK_BACKUP_COMMAND = ' && '.join([
	'echo -n "CURRENT DATETIME: "',
	'date',
	'echo',
	'sudo ntpdate-debian -qv',
	'echo',
	'bash' # Mantieni aperta la finestra lanciando una nuova sessione
])

###

import os
import subprocess
from boto import ec2
from colorama import Fore, Back, Style

execfile(os.path.abspath(os.path.dirname(__file__)) + '/commons.py')
printTitle('SYSTEM DATE/TIME CHECK', 'Connects to all instances and checks the date-time offset')
print 

connection = ec2.connect_to_region(REGION, profile_name = PROFILE_NAME)

# Ask which instances
instances = []
for instance in connection.get_only_instances():
	if instance.state == 'running' and instance.platform != 'windows':
		instance_name = instance.tags.get('Name', '(no name)')
		instances.append({ 'instance': instance, 'instance_name': instance_name })

if len(instances) > 0:
	
	# Escape command
	CHECK_BACKUP_COMMAND = CHECK_BACKUP_COMMAND.replace("\\", "\\\\").replace("'", "'\\''").replace('"', '\\"')
	
	# SSH certificates
	certificates = (SSH_CERTIFICATE if isinstance(SSH_CERTIFICATE, list) else [SSH_CERTIFICATE])
	certificates_command = ' '.join(['-i "' + path + '"' for path in certificates])
	
	# Start SSH on instances
	for instance in instances:
		instance_dns = instance['instance'].public_dns_name
		instance_ip = instance['instance'].ip_address.strip()
		terminal_title = instance['instance_name'] + ' (' + (instance_ip or instance_dns) + ')'
		subprocess.call(TERMINAL + ' --title="' + terminal_title + '" --command=\'ssh -t ' + certificates_command + ' ubuntu@' + (instance_ip or instance_dns) + ' "' + CHECK_BACKUP_COMMAND + '"\'', shell=True)
	
