#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import html
import re

from lltk.scraping import DictScraper, register

class PonsDe(DictScraper):

	def __init__(self, word):

		super(PonsDe, self).__init__(word)
		self.name = 'Pons.eu'
		self.url = 'http://de.pons.eu/dict/search/results/?q=%s&l=dede' % self.word
		self.baseurl = 'http://de.pons.eu'
		self.language = 'de'

	def _normalize(self, string):
		''' Returns a sanitized string. '''

		string = string.replace(u'\xb7', '')
		string = string.replace(u'\u0331', '')
		string = string.replace(u'\u0323', '')
		string = string.strip(' \n\rI.')
		return string

	def download(self):

		super(PonsDe, self).download()
		if self.tree.xpath('//div[@class="error"]'):
			# We're going too fast. Too many queries in a short time
			from lltk.exceptions import GoingTooFast
			raise GoingTooFast('Too many queries in a short time. Hit the break.')

	@DictScraper._needs_download
	def getelements(self):

		self.elements = []
		for element in self.tree.xpath('//div[contains(@class, "romhead")]/h2'):
			content = self._normalize(element.text_content())
			self.elements.append(content)

	@DictScraper._needs_elements
	def pos(self, element = None):
		''' Tries to decide about the part of speech. '''

		tags = []
		if element:
			if element.startswith(('der', 'die', 'das')):
				tags.append('NN')
			if ' VERB' in element:
				tags.append('VB')
			if ' ADJ' in element:
				tags.append('JJ')
		else:
			for element in self.elements:
				if self.word in unicode(element):
					return self.pos(element)
		return tags

	@DictScraper._needs_elements
	def articles(self):
		''' Tries to scrape the correct articles for singular and plural from de.pons.eu. '''

		result = [None, None]
		element = self._first('NN')
		if element:
			result[0] = [element.split(' ')[0].replace('(die)', '').strip()]
			if 'kein Plur' in element:
				# There is no plural
				result[1] = ['']
			else:
				# If a plural form exists, there is only one possibility
				result[1] = ['die']
		return result

	@DictScraper._needs_elements
	def plural(self):
		''' Tries to scrape the plural version from pons.eu. '''

		element = self._first('NN')
		if element:
			if 'kein Plur' in element:
				# There is no plural
				return ['']
			if re.search(', ([\w|\s|/]+)>', element, re.U):
				# Plural form is provided
				return re.findall(', ([\w|\s|/]+)>', element, re.U)[0].split('/')
			if re.search(', -(\w+)>', element, re.U):
				# Suffix is provided
				suffix = re.findall(', -(\w+)>', element, re.U)[0]
				return [self.word + suffix]
			if element.endswith('->'):
				# Plural is the same as singular
				return [self.word]
		return [None]

register(PonsDe)
