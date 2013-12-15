#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import html
import re

from ...scraping import Scraper

class VandaleNl(Scraper):

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

	@Scraper.needs_download
	def getelements(self):
		self.elements = []
		for element in self.tree.xpath('//div[@id="content-area"]/span[@class="f0f"]'):
			content = self._normalize(element.text_content())
			if not content.startswith(self.word + ' '):
				# This is not the word we are looking for. Throw it away...
				continue
			self.elements.append(content)

	@Scraper.needs_elements
	def article(self):
		''' Try to scrape the correct articles for singular and plural from vandale.nl. '''

		articles = [None, None]
		if len(self.elements):
			for element in self.elements:
				if re.search('([\w|\s]+) \(([\w|\s]+), (heeft [\w|\s]+)\)', element) or 'bijvoeglijk naamwoord' in element or 'bijwoord' in element:
					# Skip verbs and adjectives
					continue
				if re.search('\((de|het);', element):
					# Extract singular article
					articles[0] = re.findall('\((de|het);', element)
				else:
					# No information about the article. It's propably not a noun
					continue
				if re.search('meervoud: (\w+)', element):
					# It's a noun with a plural form
					articles[1] = ['de']
				else:
					# It's probably a noun without a plural form
					articles[1] = ['']
				return articles
		return articles

	@Scraper.needs_elements
	def plural(self):
		''' Try to scrape the plural version from vandale.nl. '''

		if len(self.elements):
			for element in self.elements:
				if re.search('([\w|\s]+) \(([\w|\s]+), (heeft [\w|\s]+)\)', element) or 'bijvoeglijk naamwoord' in element or 'bijwoord' in element:
					# Skip verbs and adjectives
					continue
				if re.search('meervoud: (\w+)', element):
					return re.findall('meervoud: (\w+)', element)
				else:
					return ['']
		return [None]

	@Scraper.needs_elements
	def conjugate(self):
		''' Try to conjugate a given verb using vandale.nl '''

		conjugation = [None, None, None]
		if len(self.elements):
			for element in self.elements:
				if re.search('([\w|\s]+) \(([\w|\s]+), (heeft [\w|\s]+)\)', element):
					conjugation[0], conjugation[1], conjugation[2] = re.findall('([\w|\s]+) \(([\w|\s]+), (heeft [\w|\s]+)\)', element)[0]
					conjugation = [x.split(' of ') for x in conjugation]
					return conjugation
		return conjugation

	@Scraper.needs_elements
	def miniaturize(self):
		''' Try to scrape the miniaturized version from vandale.nl. '''

		if len(self.elements):
			for element in self.elements:
				if re.search('([\w|\s]+) \(([\w|\s]+), (heeft [\w|\s]+)\)', element) or 'bijvoeglijk naamwoord' in element:
					# Skip verbs and adjectives
					continue
				if re.search('verkleinwoord: (\w+)', element):
					return re.findall('verkleinwoord: (\w+)', element)
				else:
					return ['']
		return [None]

	@Scraper.needs_elements
	def isnoun(self):
		''' Try to decide whether a given word is a noun using vandale.nl. '''

		if len(self.elements):
			for element in self.elements:
				if re.search('\((de|het);', element) or re.search('meervoud: (\w+)', element):
					return True
		return False

	@Scraper.needs_elements
	def isverb(self):
		''' Try to decide whether a given word is a verb using vandale.nl. '''

		if len(self.elements):
			for element in self.elements:
				if re.search('([\w|\s]+) \(([\w|\s]+), (heeft [\w|\s]+)\)', element):
					return True
		return False

	@Scraper.needs_elements
	def isadjective(self):
		''' Try to decide whether a given word is an adjective using vandale.nl. '''

		if len(self.elements):
			for element in self.elements:
				if 'bijvoeglijk naamwoord' in element and not 'bijwoord' in element:
					return True
		return False
