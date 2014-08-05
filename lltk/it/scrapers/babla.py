#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import html
import re

from lltk.scraping import DictScraper, register

class BablaIt(DictScraper):

	def __init__(self, word):

		super(BablaIt, self).__init__(word)
		self.name = 'Bab.la'
		self.url = 'http://it.bab.la/dizionario/italiano-inglese/%s' % self.word
		self.baseurl = 'http://it.bab.la/'
		self.language = 'it'

	def _normalize(self, string):
		''' Returns a sanitized string. '''

		string = string.strip()
		return string

	@DictScraper._needs_download
	def getelements(self):

		self.elements = []
		for element in self.tree.xpath('//section[1]/div[contains(@class, "result-block")]/div/div/div/p'):
			content = self._normalize(element.text_content())
			self.elements.append(content)

	@DictScraper._needs_elements
	def pos(self, element = None):
		''' Tries to decide about the part of speech. '''

		tags = []
		if element:
			if re.findall('\w+ {[m|f]}', element, re.U):
				tags.append('NN')
			if re.search('\w+ \[[\w|\|]+\]', element, re.U):
				tags.append('VB')
			if '{agg.}' in element:
				tags.append('JJ')
		else:
			for element in self.elements:
				if self.word in unicode(element):
					return self.pos(element)
		return tags

	@DictScraper._needs_elements
	def gender(self):
		''' Tries to scrape the gender for a given noun from babl.la. '''

		element = self._first('NN')
		if element:
			if re.search('{([m|f|n)])}', element, re.U):
				genus = re.findall('{([m|f|n)])}', element, re.U)[0]
				return genus

register(BablaIt)
