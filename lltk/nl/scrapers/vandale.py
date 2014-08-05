#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import html
import re

from lltk.scraping import DictScraper, register

class VandaleNl(DictScraper):

	def __init__(self, word):
		super(VandaleNl, self).__init__( word)
		self.name = 'Vandale.nl'
		self.url = 'http://www.vandale.nl/opzoeken?pattern=%s&lang=nn' % self.word
		self.baseurl = 'http://vandale.nl'
		self.language = 'nl'

	def _normalize(self, string):
		string = string.replace(u'\xb7', '')
		while string[0].isdigit():
			string = string[1:]
		return string

	@DictScraper._needs_download
	def getelements(self):
		self.elements = []
		for element in self.tree.xpath('//div[@id="content-area"]/span[@class="f0f"]'):
			content = self._normalize(element.text_content())
			if not content.startswith(self.word + ' '):
				# This is not the word we are looking for. Throw it away...
				continue
			self.elements.append(content)

	@DictScraper._needs_elements
	def pos(self, element = None):
		''' Tries to decide about the part of speech. '''

		tags = []
		if element:
			if re.search('(de|het/?de|het);', element, re.U):
				tags.append('NN')
			if re.search('[\w|\s]+ \([\w|\s]+, [\w|\s|,]+\)', element, re.U):
				tags.append('VB')
			if 'bijvoeglijk naamwoord' in element or 'bijwoord' in element:
				tags.append('JJ')
			return tags
		else:
			for element in self.elements:
				if self.word in unicode(element):
					tag = self.pos(element)
					if tag:
						return tag

	@DictScraper._needs_elements
	def articles(self):
		''' Tries to scrape the correct articles for singular and plural from vandale.nl. '''

		result = [None, None]
		element = self._first('NN')
		if element:
			if re.search('(de|het/?de|het);', element, re.U):
				result[0] = re.findall('(de|het/?de|het);', element, re.U)[0].split('/')
			if re.search('meervoud: (\w+)', element, re.U):
				# It's a noun with a plural form
				result[1] = ['de']
			else:
				# It's a noun without a plural form
				result[1] = ['']
		return result

	@DictScraper._needs_elements
	def plural(self):
		''' Tries to scrape the plural version from vandale.nl. '''

		element = self._first('NN')
		if element:
			if re.search('meervoud: ([\w|\s|\'|\-|,]+)', element, re.U):
				results = re.search('meervoud: ([\w|\s|\'|\-|,]+)', element, re.U).groups()[0].split(', ')
				results = [x.replace('ook ', '').strip() for x in results]
				return results
			else:
				# There is no plural form
				return ['']
		return [None]

	@DictScraper._needs_elements
	def miniaturize(self):
		''' Tries to scrape the miniaturized version from vandale.nl. '''

		element = self._first('NN')
		if element:
			if re.search('verkleinwoord: (\w+)', element, re.U):
				return re.findall('verkleinwoord: (\w+)', element, re.U)
			else:
				return ['']
		return [None]

register(VandaleNl)
