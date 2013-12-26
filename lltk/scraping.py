#!/usr/bin/python
# -*- coding: UTF-8 -*-

__all__ = ['register', 'discover', 'GenericScraper', 'TextScraper', 'DictScraper']

import requests
from lxml import html
from functools import wraps

class GenericScraper(object):
	''' This is the generic base class that all custom scrapers should be derived from. '''

	def __init__(self, word, language = ''):

		self.word = unicode(word)
		self.name = 'Unknown'
		self.license = None
		self.url = ''
		self.baseurl = ''
		self.language = language
		self.page = None
		self.tree = None

	def __str__(self):
		return '%s (%s): %s' % (self.name, self.baseurl, self.url)

	@classmethod
	def _needs_download(self, f):
		''' Decorator used to make sure that the downloading happens prior to running the task. '''

		@wraps(f)
		def wrapper(self, *args, **kwargs):
			if not self.isdownloaded():
				self.download()
			return f(self, *args, **kwargs)
		return wrapper

	def download(self):
		''' Download HTML from baseurl. '''

		self.page = requests.get(self.url)
		self.tree = html.fromstring(self.page.text)

	def pos(self):
		''' Try to decide about the part of speech. '''
		return []

	def isdownloaded(self):
		return bool(self.page)

	def isnoun(self):
		''' Try to decide whether a given word is a noun. '''

		if 'NN' in self.pos():
			return True
		return False

	def isverb(self):
		''' Try to decide whether a given word is a verb. '''

		if 'VB' in self.pos():
			return True
		return False

	def isadjective(self):
		''' Try to decide whether a given word is an adjective. '''

		if 'JJ' in self.pos():
			return True
		return False

	def hasplural(self):
		''' Try to find out whether a given noun has a plural form. '''

		plural = self.plural()
		if plural == ['']:
			return False
		if plural[0]:
			return True
		return None

class DictScraper(GenericScraper):
	''' DictScraper should be used for dictionary-like sites (more than one result). '''

	def __init__(self, word):

		super(DictScraper, self).__init__(word)
		self.elements = None

	@classmethod
	def _needs_elements(self, f):
		''' Decorator used to make sure that there are elements prior to running the task. '''

		@wraps(f)
		def wrapper(self, *args, **kwargs):
			if self.elements == None:
				self.getelements()
			return f(self, *args, **kwargs)
		return wrapper

	def _first(self, tag):
		''' Return the first element with required POS-tag. '''

		self.getelements()
		for element in self.elements:
			if tag in self.pos(element):
				return element
		return None

class TextScraper(GenericScraper):
	''' TextScraper should be used for text-like sites (one result) such as Wiktionary. '''

	def __init__(self, word):
		super(TextScraper, self).__init__(word)
