#!/usr/bin/python
# -*- coding: UTF-8 -*-

def interactiveconsole(vars):
	''' Opens an interactive python console for debug purposes. '''

	import readline
	from code import InteractiveConsole

	shell = InteractiveConsole(vars)
	shell.interact()

	# Then do something like:
	# html.open_in_browser(tree, encoding = 'utf-8')

def trace(f, *args, **kwargs):
	''' Decorator used to trace function calls for debugging purposes. '''

	print 'Calling %s() with args %s, %s ' %(f.__name__, args, kwargs)
	return f(*args,**kwargs)
