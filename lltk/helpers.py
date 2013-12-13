#!/usr/bin/python
# -*- coding: UTF-8 -*-

def trace(f, *args, **kwargs):
	''' Decorator used to trace function calls for debugging purposes. '''

	print 'Calling %s() with args %s, %s ' %(f.__name__, args, kwargs)
	return f(*args,**kwargs)
