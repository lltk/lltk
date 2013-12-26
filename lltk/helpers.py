#!/usr/bin/python
# -*- coding: UTF-8 -*-

def debug(message):
	''' Prints message if debug mode is enabled. '''

	from lltk import DEBUG
	if DEBUG:
		from termcolor import colored
		print colored('@LLTK-DEBUG: ' + message, 'yellow')

def debugconsole():
	''' Opens an interactive IPython console. Used for debugging purposes. '''

	from IPython import embed
	embed()

def trace(f, *args, **kwargs):
	''' Decorator used to trace function calls for debugging purposes. '''

	print 'Calling %s() with args %s, %s ' % (f.__name__, args, kwargs)
	return f(*args,**kwargs)
