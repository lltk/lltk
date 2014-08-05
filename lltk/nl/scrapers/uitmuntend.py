#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import html
import re

from lltk.scraping import DictScraper, register

class UitmuntendNl(DictScraper):

	def __init__(self, word):

		super(UitmuntendNl, self).__init__(word)
		self.name = 'Uitmuntend.de'
		self.url = 'http://www.uitmuntend.de/woordenboek/%s/' % self.word
		self.baseurl = 'http://uitmuntend.de'
		self.language = 'nl'

	def _normalize(self, string):
		''' Returns a sanitized string. '''

		#string = re.sub(' \[[m|f|n|p]+?\]', '', string)
		string = string.replace(' [p]', '')
		return string

	@DictScraper._needs_download
	def getelements(self):

		self.elements = []
		for element in self.tree.xpath('//div[@id="wb_resultaten"]//tr')[2:]:
			content = self._normalize(element.text_content())
			if content.startswith('\r'):
				continue
			if content.startswith('Zusammensetzungen'):
				break
			self.elements.append(content)

	@DictScraper._needs_elements
	def pos(self, element = None):
		''' Tries to decide about the part of speech. '''

		tags = []
		if element:
			if element.startswith(('de ', 'het ', 'het/de', 'de/het')) and not re.search('\[[\w|\s][\w|\s]+\]', element.split('\r\n')[0], re.U):
				tags.append('NN')
			if re.search('[\w|\s|/]+ \| [\w|\s|/]+ - [\w|\s|/]+', element, re.U):
				tags.append('VB')
			if re.search('[\w|\s]+ \| [\w|\s]+', element, re.U):
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
		''' Tries to scrape the correct articles for singular and plural from uitmuntend.nl. '''

		result = [None, None]
		element = self._first('NN')
		if element:
			element = element.split('\r\n')[0]
			if ' | ' in element:
				# This means there is a plural
				singular, plural = element.split(' | ')
				singular, plural = singular.strip(), plural.strip()
			else:
				# This means there is no plural
				singular, plural = element.strip(), ''
				result[1] = ''
			if singular:
				result[0] = singular.split(' ')[0].split('/')
			if plural:
				result[1] = plural.split(' ')[0].split('/')
		return result

	@DictScraper._needs_elements
	def plural(self):
		''' Tries to scrape the plural version from uitmuntend.nl. '''

		element = self._first('NN')
		if element:
			element = element.split('\r\n')[0]
			if ' | ' in element:
				# This means there is a plural
				singular, plural = element.split(' | ')
				return [plural.split(' ')[1]]
			else:
				# This means there is no plural
				return ['']
		return [None]

	@DictScraper._needs_elements
	def gender(self):
		''' Tries to scrape the gender for a given noun from uitmuntend.nl. '''

		element = self._first('NN')
		if element:
			element = element.split('\r\n')[0]
			if re.search(r' \[([m|f])\]', element, re.U):
				genus = re.findall(r' \[([m|f])\]', element, re.U)[0]
				return genus
			return 'n'

register(UitmuntendNl)
