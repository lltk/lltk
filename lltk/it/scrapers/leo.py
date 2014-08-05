#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import html
import re

from lltk.scraping import DictScraper, register

class LeoIt(DictScraper):

	def __init__(self, word):

		super(LeoIt, self).__init__(word)
		self.name = 'Leo.org'
		self.url = 'http://dict.leo.org/dictQuery/m-vocab/itde/de.html?lp=itde&search=%s' % self.word
		self.baseurl = 'http://dict.leo.org/itde/'
		self.language = 'it'

	def _normalize(self, string):
		''' Returns a sanitized string. '''

		string = string.replace(u'\xa0', ' ')
		string = string.strip()
		return string

	@DictScraper._needs_download
	def getelements(self):

		self.elements = []
		for element in self.tree.xpath('//div[contains(@id, "section-subst")]//td[contains(@lang, "it")]'):
			content = self._normalize(element.text_content())
			content = [x.strip() for x in content.split('|')]
			content = [x for x in content if x.startswith(self.word)]
			self.elements += content
		for element in self.tree.xpath('//div[contains(@id, "section-adjadv")]//td[contains(@lang, "it")]'):
			content = self._normalize(element.text_content())
			self.elements.append(content)
		for element in self.tree.xpath('//div[contains(@id, "section-verb")]//td[contains(@lang, "it")]'):
			content = self._normalize(element.text_content())
			if content.startswith(self.word):
				self.elements.append(content + ' [VERB]')

	@DictScraper._needs_elements
	def pos(self, element = None):
		''' Tries to decide about the part of speech. '''

		tags = []
		if element:
			if re.search('[\w|\s]+ [m|f]\.', element, re.U):
				tags.append('NN')
			if '[VERB]' in element:
				tags.append('VB')
			if 'adj.' in element and re.search('([\w|\s]+, [\w|\s]+)', element, re.U):
				tags.append('JJ')
		else:
			for element in self.elements:
				if element.startswith(self.word):
					tags += self.pos(element)
		return list(set(tags))

	@DictScraper._needs_elements
	def gender(self):
		''' Tries to scrape the gender for a given noun from leo.org. '''

		element = self._first('NN')
		if element:
			if re.search('([m|f|n)])\.', element, re.U):
				genus = re.findall('([m|f|n)])\.', element, re.U)[0]
				return genus

register(LeoIt)
