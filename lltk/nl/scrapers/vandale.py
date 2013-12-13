#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import html

from ...scraping import Scraper

class VandaleNl(Scraper):

	def __init__(self, word):
		super(VandaleNl, self).__init__( word)
		self.name = 'Vandale.nl'
		self.url = 'http://www.vandale.nl/opzoeken?pattern=%s&lang=nn' % self.word
		self.baseurl = 'http://vandale.nl'
		self.language = 'nl'

	def download(self):
		super(VandaleNl, self).download()
		if self.tree.xpath('//div[@class="error"]'):
			# We're going too fast. Too many queries in a short time
			from ..exceptions import GoingTooFast
			raise GoingTooFast('Too many queries in a short time. Hit the break.')

	@Scraper.needs_download
	def article(self):
		''' Try to scrape the correct articles for singular and plural from vandale.nl. '''

		result = [None, None]
		elements = self.tree.xpath('//span[@class="f0f"]/span[@class="f0j"]')
		if len(elements):
			elements = elements[0].getchildren()
			element = [element.text for element in elements]

			while element[0].isdigit():
				element = element[1:]
			singular = ''.join(element[0:element.index(' ')]).replace(u'\xb7', '')
			if not singular == self.word:
				return [None, None]

			element = [singular] + element[element.index(' ') + 1:]
			if element[2] in ['de', 'het', 'de/het', 'het/de']:
				result[0] = element[2]
			else:
				# No article specified. Let's say it's 'de'
				result[0] = 'de'

			if not 'meervoud: ' in element:
				# This means there is no plural
				result[1] = ''
			else:
				result[1] = 'de'

		return result

	@Scraper.needs_download
	def plural(self):
		''' Try to scrape the plural version from vandale.nl. '''

		elements = self.tree.xpath('//span[@class="f0f"]/span[@class="f0j"]')
		if len(elements):
			elements = elements[0].getchildren()
			element = [element.text for element in elements]

			while element[0].isdigit():
				element = element[1:]
			singular = ''.join(element[0:element.index(' ')]).replace(u'\xb7', '')
			if not singular == self.word:
				return [None]

			if 'meervoud: ' in element:
				first = element.index('meervoud: ') + 1
				plurals = element[first:][:element[first:].index(')')]
				if ', ' in plurals:
					plurals.remove(', ')
				return plurals
			else:
				# This means there is no plural
				return ['']

		return [None]

	@Scraper.needs_download
	def miniaturize(self):
		''' Try to scrape the miniaturized version from vandale.nl. '''

		elements = self.tree.xpath('//span[@class="f0f"]/span[@class="f0j"]')[0].getchildren()
		element = [element.text for element in elements]

		while element[0].isdigit():
			element = element[1:]
		singular = ''.join(element[0:element.index(' ')]).replace(u'\xb7', '')
		if singular is not self.word:
			return [None]

		if 'verkleinwoord: ' in element:
			miniature = element[element.index('verkleinwoord: ') + 1]
			return [miniature]
		else:
			# This means there is no miniature form
			return ['']
		return [None]
