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
		def wrapper(self, *args, **kwargs):
			if not self.is_downloaded():
				self.download()
			return f(self, *args, **kwargs)
		return wrapper

	@classmethod
	def needs_elements(self, f):
		def wrapper(self, *args, **kwargs):
			if self.elements == None:
				self.getelements()
			return f(self, *args, **kwargs)
		return wrapper

	def download(self):
		self.page = requests.get(self.url)
		self.tree = html.fromstring(self.page.text)

	def is_downloaded(self):
		return bool(self.page)
