#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import html

from ...scraping import Scraper

class WiktionaryIt(Scraper):

	def __init__(self, word):
		super(WiktionaryIt, self).__init__(word)
		self.name = 'Wiktionary.org'
		self.url = 'http://it.wiktionary.org/wiki/%s' % self.word
		self.baseurl = 'http://it.wiktionary.org'
		self.language = 'it'

	@Scraper.needs_download
	def ipa(self):
		result = self.tree.xpath('//span[@class="IPA"]/text()')
		if len(result):
			if not result[0].startswith('/') and not result[0].endswith('/'):
				result[0] = '/' + result[0] + '/'
			return [result[0]]
		else:
			for char in [('a', 'o'), ('i', 'o'), ('e', 'a')]:
				if self.word.endswith(char[0]):
					result = ipa(self.word[:-1] + char[1])
					if result[0]:
						return [result[0][:-2] + str(char[0]) + '/']
		return [None]
