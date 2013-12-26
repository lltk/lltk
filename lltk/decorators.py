#!/usr/bin/python
# -*- coding: UTF-8 -*-

from functools import wraps

def _load_language(f):
	''' Decorator used to load a custom method for a given language. '''

	# This decorator checks if there's a custom method for a given language.
	# If so, prefer the custom method, otherwise do nothing.

	@wraps(f)
	def loader(language, word, *args, **kwargs):
		method = f.func_name
		try:
			if isinstance(language, (list, tuple)):
				_lltk = __import__('lltk.' + language[0], globals(), locals(), [method], -1)
			else:
				_lltk = __import__('lltk.' + language, globals(), locals(), [method], -1)
		except ImportError:
			from exceptions import LanguageNotSupported
			raise LanguageNotSupported('The language ' + language.upper() + ' is not supported so far.')
		try:
			function = eval('_lltk.' + method)
			return function(word)
		except (TypeError, AttributeError) as e:
			# No custom method implemented, yet. Continue as normal...
			return f(language, word, *args, **kwargs)
	return loader

def _load_language_or_die(f):
	''' Decorator used to load a custom method for a given language. '''

	# This decorator checks if there's a custom method for a given language.
	# If so, prefer the custom method, otherwise raise exception NotImplementedError.

	@wraps(f)
	def loader(language, word, *args, **kwargs):
		method = f.func_name
		try:
			if isinstance(language, (list, tuple)):
				_lltk = __import__('lltk.' + language[0], globals(), locals(), [method], -1)
			else:
				_lltk = __import__('lltk.' + language, globals(), locals(), [method], -1)
		except ImportError:
			from exceptions import LanguageNotSupported
			raise LanguageNotSupported('The language ' + language.upper() + ' is not supported so far.')
		try:
			function = eval('_lltk.' + method)
			return function(word)
		except (TypeError, AttributeError) as e:
			# No custom method implemented, yet.
			raise NotImplementedError('Method lltk.' + language + '.' + method +'() not implemented, yet.')
	return loader
