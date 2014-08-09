#!/usr/bin/python
# -*- coding: UTF-8 -*-

__all__ = ['download', 'play', 'debug', 'open_in_browser', 'debugconsole', 'trace']

def download(url, filename, overwrite = False):
	''' Downloads a file via HTTP. '''

	from requests import get
	from os.path import exists

	debug('Downloading ' + unicode(url) + '...')
	data = get(url)
	if data.status_code == 200:
		if not exists(filename) or overwrite:
			f = open(filename, 'wb')
			f.write(data.content)
			f.close()
		return True
	return False

def play(filename):
	''' Uses /usr/bin/mpg123 to play MP3 files. '''

	from subprocess import call
	call(['/usr/bin/mpg123', '-q', filename])

def debug(message):
	''' Prints a message if debug mode is enabled. '''

	import lltk.config as config
	if config['debug']:
		from termcolor import colored
		print colored('@LLTK-DEBUG: ' + message, 'yellow')

def open_in_browser(tree, encoding = 'utf-8'):
	''' Opens a LXML tree in a browser. '''

	from lxml.html import open_in_browser
	open_in_browser(tree, encoding)

def debugconsole():
	''' Opens an interactive IPython console. Used for debugging purposes. '''

	from IPython import embed
	embed()

def trace(f, *args, **kwargs):
	''' Decorator used to trace function calls for debugging purposes. '''

	print 'Calling %s() with args %s, %s ' % (f.__name__, args, kwargs)
	return f(*args,**kwargs)
