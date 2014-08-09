#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import html
import re

from lltk.scraping import TextScraper, register

class WiktionaryIt(TextScraper):

	def __init__(self, word):

		super(WiktionaryIt, self).__init__(word)
		self.name = 'Wiktionary.org'
		self.url = 'http://it.wiktionary.org/wiki/%s' % self.word
		self.baseurl = 'http://it.wiktionary.org'
		self.language = 'it'

#	def _normalize(self, string):
#		''' Returns a sanitized string. '''

#		string = string.replace(u'\xb7', '')
#		string = string.strip()
#		return string

	@TextScraper._needs_download
	def pos(self):
		''' Tries to decide about the part of speech. '''

		tags = []
		if self.tree.xpath('//div[@id="mw-content-text"]/h3/span/i/a/text()'):
			info = self.tree.xpath('//div[@id="mw-content-text"]/h3/span/i/a/text()')
			if 'Sostantivo' in info:
				tags.append('NN')
			if 'Verbo' in info:
				tags.append('VB')
			if 'Aggettivo' in info:
				tags.append('JJ')
		return tags

	@TextScraper._needs_download
	def ipa(self):

		result = self.tree.xpath('//div[@id="mw-content-text"]//span[@class="IPA"]/text()')
		if result:
			result = result[0]
			result = result.strip('/')
			return [result]
		return [None]

	@TextScraper._needs_download
	def gender(self):

		if self.tree.xpath('//div[@id="mw-content-text"]/h3/span[@id="Sostantivo"]'):
			content = self.tree.xpath('//div[@id="mw-content-text"]/h3/span[@id="Sostantivo"]')[0].getparent().getnext().text_content()
			if re.search(' ([m|f]) ', content):
				genus = re.findall(' ([m|f]) ', content)[0]
				return genus

#	@TextScraper._needs_download
#	def articles(self):

#		result = [None, None]
#		if self.pos() == 'NN':
#			if self.tree.xpath('//table[contains(@class, "wikitable")]/tr'):
#				content = self.tree.xpath('//table[contains(@class, "wikitable")]/tr')[1].text_content()
#				singular, plural = content.split('\n')[1:3]
#				if singular.startswith(('der ', 'die ', 'das ')):
#					result[0] = singular.split(' ')[0]
#				if plural.startswith(('der ', 'die ', 'das ')):
#					result[1] = plural.split(' ')[0]
#		return result

#	@TextScraper._needs_download
#	def plural(self):

#		if self.pos() == 'NN':
#			if self.tree.xpath(u'//div[@id="mw-content-text"]/p[@title="Trennungsmöglichkeiten am Zeilenumbruch"]'):
#				content = self._normalize(self.tree.xpath(u'//div[@id="mw-content-text"]/p[@title="Trennungsmöglichkeiten am Zeilenumbruch"]')[0].getnext().text_content())
#				result = re.findall('Plural[\d|\s]*: ([\w|\s]+)', content, re.U)
#				result = [x.strip() for x in result]
#				return result
#		return [None]

register(WiktionaryIt)
