#!/usr/bin/python
# -*- coding: UTF-8 -*-

def load_language(f):
	''' This decorator checks if there's a custom method for a given language. If so, prefer the custom method, otherwise do nothing. '''

	# @TODO: Modify docstrings
	def loader(*args, **kwargs):
		language, word, functionality = args[0], args[1], f.func_name
		try:
			_lltk = __import__('lltk.' + language, globals(), locals(), [functionality], -1)
		except ImportError:
			from exceptions import LanguageNotSupported
			raise LanguageNotSupported('The language ' + language.upper() + ' is not supported so far.')
		try:
			function = eval('_lltk.' + functionality)
			return function(word)
		except (TypeError, AttributeError):
			# No custom method implemented, yet. Continue as normal...
			return f(*args, **kwargs)
	return loader

def load_language_or_die(f):
	''' This decorator loads a custom method for a given language. '''

	def loader(*args, **kwargs):
		language, word, functionality = args[0], args[1], f.func_name
		try:
			_lltk = __import__('lltk.' + language, globals(), locals(), [functionality], -1)
		except ImportError:
			from exceptions import LanguageNotSupported
			raise LanguageNotSupported('The language ' + language.upper() + ' is not supported so far.')
		try:
			function = eval('_lltk.' + functionality)
			return function(word)
		except (TypeError, AttributeError):
			# No custom method implemented, yet.
			raise NotImplementedError('Method lltk.' + language + '.' + functionality +'() not implemented, yet.')
			# Do this if you want to continue as normal:
			# return f(*args, **kwargs)
	return loader
