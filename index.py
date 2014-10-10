# -*- coding: utf-8 -*-

### AN INTERACTIVE MENU TO RUN UTILITIES
### Lists all script in the folder and asks which to execute

import os
import sys
from colorama import Fore, Back, Style

execfile(os.path.abspath(os.path.dirname(__file__)) + '/commons.py')
printTitle('AWS INTERACTIVE UTILS', 'A set of scripts to interactively perform common tasks on AWS')

def file_compare(x, y): 
	return cmp(x.replace('_', '~').lower(), y.replace('_', '~').lower())

def make_label(filename): 
	return ' '.join(j[0].upper()+j[1:] for j in filename[0:-3].replace('_', ' ').strip(' _').split())

# Get the files list
directory = os.path.abspath(os.path.dirname(__file__))
files = os.listdir(directory)
files.sort(cmp = file_compare)

# Build the scripts list
scripts = []
for script in files:
	if script[-3:] == '.py' and script[0:7] != 'commons' and script != 'index.py' and script[0] != '.':
		scripts.append({ 'filename': script, 'label': make_label(script) })

# Loop on scripts
while True:
	print Style.RESET_ALL
	
	# Print menu
	index = 1
	for script in scripts:
		print (Style.BRIGHT + '{:3d}: ' + Fore.BLUE + '{}' + Style.RESET_ALL).format(index, script['label'])
		index += 1
	print
	
	# Parse selection
	selection = -1
	while selection < 0 or selection >= len(scripts):
		selection = raw_input('Type a number to select, or press ENTER to exit: ').strip()
		if selection == '': 
			exit(0)
		if not selection.isdigit():
			continue
		selection = int(selection.strip()) - 1
	
	try:
		print
		execfile(directory + '/' + scripts[selection]['filename'])
		
	except Exception as x:
		print
		print Fore.RED + Style.BRIGHT + 'ERROR: ' + Style.NORMAL,
		print x,
		print Style.RESET_ALL
		print
