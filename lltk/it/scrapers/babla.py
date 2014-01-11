#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import html
import re

from ...scraping import DictScraper, register

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
		''' Try to decide about the part of speech. '''

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
		''' Try to scrape the gender for a given noun from babl.la. '''

		element = self._first('NN')
		if element:
			if re.search('{([m|f|n)])}', element, re.U):
				genus = re.findall('{([m|f|n)])}', element, re.U)[0]
				return genus

#	@DictScraper._needs_elements
#	def conjugate(self):
#		''' Try to conjugate a given verb using bab.la.'''

#		conjugation = [None, None, None]
#		element = self._first('VB')
#		if element:
#			conjugation[0] = self.word
#			conjugation[1], conjugation[2] = re.findall('\w+ \[(\w+)\|(\w+)\]', element, re.U)[0]
#			conjugation = [x.split('/') for x in conjugation]
#		return conjugation

register('it', BablaIt)
