#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import html

from ...scraping import Scraper

class WiktionaryDe(Scraper):

	def __init__(self, word):
		super(WiktionaryDe, self).__init__(word)
		self.name = 'Wiktionary.org'
		self.url = 'http://de.wiktionary.org/wiki/%s' % self.word
		self.baseurl = 'http://de.wiktionary.org'
		self.language = 'de'

	@Scraper.needs_download
	def ipa(self):
		result = self.tree.xpath('//span[@class="ipa"]/text()')
		result = filter(lambda x: x != u'\u2026', result)
		if len(result):
			if not result[0].startswith('/') and not result[0].endswith('/'):
				result[0] = '/' + result[0] + '/'
			return [result[0]]
		return [None]
