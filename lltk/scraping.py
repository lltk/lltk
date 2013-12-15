#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import html

class Scraper(object):

	def __init__(self, word):
		self.word = unicode(word)
		self.name = 'Unknown'
		self.licence = None
		self.url = ''
		self.baseurl = ''
		self.language = ''
		self.page = None
		self.tree = None
		self.elements = None

	def __str__(self):
		return 'Scraper %s (%s): %s' % (self.name, self.baseurl, self.word)

	@classmethod
	def needs_download(self, f):
		''' Decorator used to make sure that the downloading happens prior to running the task. '''
		def wrapper(self, *args, **kwargs):
			if not self.isdownloaded():
				self.download()
			return f(self, *args, **kwargs)
		return wrapper

	@classmethod
	def needs_elements(self, f):
		''' Decorator used to make sure that there are elements prior to running the task. '''
		def wrapper(self, *args, **kwargs):
			if self.elements == None:
				self.getelements()
			return f(self, *args, **kwargs)
		return wrapper

	def download(self):
		''' Download HTML from baseurl. '''
		self.page = requests.get(self.url)
		self.tree = html.fromstring(self.page.text)

	def isdownloaded(self):
		return bool(self.page)

	def hasplural(self):
		''' Try to find out whether a given noun has a plural form. '''

		plural = self.plural()
		if plural == ['']:
			return False
		if plural[0]:
			return True
		return None
