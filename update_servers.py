# -*- coding: utf-8 -*-

### CONNECTS TO SELECTED EC2 INSTANCES VIA SSH AND RUNS UPDATE COMMANDS ON THEM
### If an instance has tag NoUpdate=1, then it's not listed and not updated

### CONFIGURATION
REGION = 'eu-west-1'
PROFILE_NAME = 'InstanceLister'
TERMINAL = 'xfce4-terminal'
SSH_CERTIFICATE = '/home/lorenzo/.certificates/david-1.pem'
UPDATE_COMMAND = ' && '.join([
	'sudo apt-get update',
	'sudo apt-get upgrade',
	'sudo apt-get clean',
	'sudo apt-get autoclean',
	'sudo apt-get autoremove',
	'if [ -f /var/run/reboot-required ]; then echo; echo "=== SYSTEM REBOOT REQUIRED! ==="; read -p "Do you want to reboot now (y|n)? " -r; if [[ $REPLY =~ ^[Yy] ]]; then sudo shutdown -r now; fi; echo; fi',
	'bash'
])

###

import os
import subprocess
from boto import ec2
from colorama import Fore, Back, Style

execfile(os.path.abspath(os.path.dirname(__file__)) + '/commons.py')
printTitle('EC2 INSTANCES UPDATE', 'Runs apt-get to update instances, excluding ones with tag NoUpdate=1')
print 

connection = ec2.connect_to_region(REGION, profile_name = PROFILE_NAME)

# Ask which instances
instances = []
for instance in connection.get_only_instances():
	if instance.state == 'running' and instance.tags.get('NoUpdate', '0') != '1' and instance.platform != 'windows':
		instance_name = instance.tags.get('Name', '(no name)')
		if questionYN('Do you want to update instance ' + Style.BRIGHT + '{}' + Style.RESET_ALL + ' ({})', instance_name, instance.id):
			instances.append({ 'instance': instance, 'instance_name': instance_name })

if len(instances) > 0:
	
	# Escape command
	UPDATE_COMMAND = UPDATE_COMMAND.replace("\\", "\\\\").replace("'", "'\\''").replace('"', '\\"')
	
	# Start SSH on instances
	for instance in instances:
		instance_dns = instance['instance'].public_dns_name
		instance_ip = instance['instance'].ip_address.strip()
		terminal_title = instance['instance_name'] + ' UPDATE (' + (instance_ip or instance_dns) + ')'
		subprocess.call(TERMINAL + ' --title="' + terminal_title + '" --command=\'ssh -t -i "' + SSH_CERTIFICATE + '" ubuntu@' + (instance_ip or instance_dns) + ' "' + UPDATE_COMMAND + '"\'', shell=True)
	
