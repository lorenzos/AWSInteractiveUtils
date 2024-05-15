# -*- coding: utf-8 -*-

from colorama import Fore, Back, Style

def printTitle(title, description):
	print(Style.BRIGHT + Fore.BLUE + title + Style.RESET_ALL)
	if description != '':
		print(Fore.BLUE + description + Style.RESET_ALL)

def questionInput(msg, *args):
	return input((msg + ': ').format(*args)).strip()

def questionYN(msg, *args):
	r = questionInput(msg + ' [y|n]', *args).lower()
	return r == 'y' or r == 'yes'
