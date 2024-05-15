# -*- coding: utf-8 -*-

### AN INTERACTIVE MENU TO RUN UTILITIES
### Lists all script in the folder and asks which to execute

import os
import sys
from colorama import Fore, Back, Style
from functools import cmp_to_key

exec(compile(open(os.path.abspath(os.path.dirname(__file__)) + '/commons.py', "rb").read(), os.path.abspath(os.path.dirname(__file__)) + '/commons.py', 'exec'))
printTitle('AWS INTERACTIVE UTILS', 'A set of scripts to interactively perform common tasks on AWS')

def cmp(a, b):
	return (a > b) - (a < b) 

def file_compare(x, y): 
	return cmp(x.replace('_', '~').lower(), y.replace('_', '~').lower())

def make_label(filename): 
	return ' '.join(j[0].upper()+j[1:] for j in filename[0:-3].replace('_', ' ').strip(' _').split())

# Get the files list
directory = os.path.abspath(os.path.dirname(__file__))
files = os.listdir(directory)
files.sort(key = cmp_to_key(file_compare))

# Build the scripts list
scripts = []
for script in files:
	if script[-3:] == '.py' and script[0:7] != 'commons' and script != 'index.py' and script[0] != '.':
		scripts.append({ 'filename': script, 'label': make_label(script) })
scripts = sorted(scripts, key=lambda d: d['label']) 

# Defalut script already selected using the first command line arg?
initial = sys.argv[1] if len(sys.argv) > 1 else None

# Loop on scripts
while True:
	print(Style.RESET_ALL)
	
	# Print menu
	index = 1
	for script in scripts:
		print((Style.BRIGHT + '{:3d}: ' + Fore.BLUE + '{}' + Style.RESET_ALL).format(index, script['label']))
		index += 1
	print()
	
	# Parse selection
	selection = -1
	if initial and initial.isdigit():
		selection = int(initial) - 1
		initial = None
	while selection < 0 or selection >= len(scripts):
		selection = input('Type a number to select, or press ENTER to exit: ').strip()
		if selection == '': 
			exit(0)
		if not selection.isdigit():
			continue
		selection = int(selection.strip()) - 1
	
	
	print()
	exec(compile(open(directory + '/' + scripts[selection]['filename'], "rb").read(), directory + '/' + scripts[selection]['filename'], 'exec'))
