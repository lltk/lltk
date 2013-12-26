#!/usr/bin/python
# -*- coding: UTF-8 -*-

def debugconsole():
	''' Opens an interactive IPython console. Used for debugging purposes. '''

	from IPython import embed
	embed()

def trace(f, *args, **kwargs):
	''' Decorator used to trace function calls for debugging purposes. '''

	print 'Calling %s() with args %s, %s ' % (f.__name__, args, kwargs)
	return f(*args,**kwargs)
