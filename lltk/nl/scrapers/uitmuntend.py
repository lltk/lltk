#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import html
import re

from ...scraping import Scraper

class UitmuntendNl(Scraper):

	def __init__(self, word):
		super(UitmuntendNl, self).__init__( word)
		self.name = 'Uitmuntend.de'
		self.url = 'http://www.uitmuntend.de/woordenboek/%s/' % self.word
		self.baseurl = 'http://uitmuntend.de'
		self.language = 'nl'

	@Scraper.needs_download
	def getelements(self):
		self.elements = []
		for element in self.tree.xpath('//div[@id="wb_resultaten"]//tr')[2:]:
			content = element.text_content()
			if content.startswith('\r'):
				continue
			if content.startswith('Zusammensetzungen'):
				break
			self.elements.append(content)

	@Scraper.needs_elements
	def article(self):
		''' Try to scrape the correct articles for singular and plural from uitmuntend.nl. '''

		articles = [None, None]
		if len(self.elements):
			for element in self.elements:
				element = element.split('\r\n')[0]
				element = re.sub(' \[[m|f|n|p]+?\]', '', element)
				if not element.startswith(('de ', 'het ')) or re.search('\[\w+\]', element):
					continue
				if ' | ' in element:
					# This means there is a plural
					singular, plural = element.split(' | ')
					singular, plural = singular.strip(), plural.strip()
				else:
					# This means there is no plural
					singular, plural = element.strip(), ''
					articles[1] = plural
				if singular:
					articles[0] = singular.split(' ')[0]
				if plural:
					articles[1] = plural.split(' ')[0]
				return articles
		return articles

	@Scraper.needs_elements
	def plural(self):
		''' Try to scrape the plural version from uitmuntend.nl. '''

		if len(self.elements):
			for element in self.elements:
				element = element.split('\r\n')[0]
				element = re.sub(' \[[m|f|n|p]+?\]', '', element)
				if not element.startswith(('de ', 'het ')) or re.search('\[\w+\]', element):
					continue
				if ' | ' in element:
					# This means there is a plural
					singular, plural = element.split(' | ')
					return [plural.split(' ')[1]]
				else:
					# This means there is no plural
					return ['']
			return [None]
		return [None]

	@Scraper.needs_elements
	def gender(self):
		''' Try to scrape the gender for a given noun from uitmuntend.nl. '''

		if len(self.elements):
			for element in self.elements:
				element = element.split('\r\n')[0]
				if not element.startswith(('de ', 'het ')):
					continue
				if re.search(r' \[([m|f|n])\]', element):
					return re.findall(r' \[([m|f|n])\]', element)[0]
				else:
					if element.startswith('het '):
						return 'n'
		return None

	@Scraper.needs_elements
	def conjugate(self):
		''' Try to conjugate a given verb using uitmuntend.nl '''

		conjugation = [None, None, None]
		if len(self.elements):
			for element in self.elements:
				element = element.split('\r\n')[0]
				if element.startswith(('de ', 'het ')) or re.search('\[\w+\]', element):
					continue
				element = element.split(' | ')
				if len(element) > 1:
					conjugation[0] = element[0].strip().split(' / ')
					element = element[1].split(' - ')
					if len(element) > 1:
						conjugation[1] = element[0].split(' / ')
						conjugation[2] = element[1].replace('|', '').strip().split(' / ')
				return conjugation
		return conjugation

	@Scraper.needs_elements
	def isnoun(self):
		''' Try to decide whether a given word is a noun using uitmuntend.nl. '''

		if len(self.elements):
			for element in self.elements:
				return element.startswith(('de ', 'het '))
		return False

	@Scraper.needs_elements
	def isverb(self):
		''' Try to decide whether a given word is a verb using uitmuntend.nl. '''

		if len(self.elements):
			for element in self.elements:
				if not element.startswith(('de ', 'het ')):
					if '- heeft' in element:
						return True
				return False
		return False

	@Scraper.needs_elements
	def isadjective(self):
		''' Try to decide whether a given word is an adjective using uitmuntend.nl. '''

		if len(self.elements):
			for element in self.elements:
				if not element.startswith(('de ', 'het ')):
					if not '- heeft' in element and ' | ' in element:
						return True
				return False
		return False
