#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import html
import re

from lltk.scraping import TextScraper, register

class WiktionaryDe(TextScraper):

	def __init__(self, word):

		super(WiktionaryDe, self).__init__(word)
		self.name = 'Wiktionary.org'
		self.url = 'http://de.wiktionary.org/wiki/%s' % self.word
		self.baseurl = 'http://de.wiktionary.org'
		self.language = 'de'

	def _normalize(self, string):
		''' Returns a sanitized string. '''

		string = string.replace(u'\xb7', '')
		string = string.replace(u'\xa0', ' ')
		string = string.replace('selten: ', '')
		string = string.replace('Alte Rechtschreibung', '')
		string = string.strip()
		return string

	@TextScraper._needs_download
	def pos(self):
		''' Tries to decide about the part of speech. '''

		tags = []
		if self.tree.xpath('//div[@id="mw-content-text"]//a[@title="Hilfe:Wortart"]/text()'):
			info = self.tree.xpath('//div[@id="mw-content-text"]//a[@title="Hilfe:Wortart"]/text()')[0]
			if info == 'Substantiv':
				tags.append('NN')
			if info == 'Verb':
				tags.append('VB')
			if info == 'Adjektiv':
				tags.append('JJ')
		return tags

	@TextScraper._needs_download
	def ipa(self):

		if self.tree.xpath('//span[@class="ipa"]/text()'):
			result = self.tree.xpath('//span[@class="ipa"]/text()')[0]
			result = result.strip('/')
			return [result]
		return [None]

	@TextScraper._needs_download
	def gender(self):

		if 'NN' in self.pos():
			if self.tree.xpath('//div[@id="mw-content-text"]//span[@class="mw-headline"]/em[contains(@title, "Genus")]/text()'):
				genus = self.tree.xpath('//div[@id="mw-content-text"]//span[@class="mw-headline"]/em[contains(@title, "Genus")]/text()')[0]
				return genus

	@TextScraper._needs_download
	def articles(self):

		result = [None, None]
		if 'NN' in self.pos():
			if self.tree.xpath('//table[contains(@class, "wikitable")]/tr'):
				content = self.tree.xpath('//table[contains(@class, "wikitable")]/tr')[1].text_content()
				singular, plural = content.split('\n')[1:3]
				if singular.startswith(('der ', 'die ', 'das ')):
					result[0] = singular.split(' ')[0].split('/')
				if plural.startswith(('der ', 'die ', 'das ')):
					result[1] = plural.split(' ')[0].split('/')
		return result

	@TextScraper._needs_download
	def plural(self):

		if 'NN' in self.pos():
			if self.tree.xpath(u'//div[@id="mw-content-text"]/p[@title="Trennungsmöglichkeiten am Zeilenumbruch"]'):
				content = self._normalize(self.tree.xpath(u'//div[@id="mw-content-text"]/p[@title="Trennungsmöglichkeiten am Zeilenumbruch"]')[0].getnext().text_content())
				result = re.findall('Plural[\d|\s]*: ([\w|\s]+)', content, re.U)
				result = [x.strip() for x in result]
				return result
		return [None]

	@TextScraper._needs_download
	def comparative(self):

		if 'JJ' in self.pos():
			if self.tree.xpath(u'//div[@id="mw-content-text"]/p[@title="Trennungsmöglichkeiten am Zeilenumbruch"]'):
				content = self._normalize(self.tree.xpath(u'//div[@id="mw-content-text"]/p[@title="Trennungsmöglichkeiten am Zeilenumbruch"]')[0].getnext().text_content())
				result = re.findall('Komparativ[\d|\s]*: ([\w|\s]+)', content, re.U)
				result = [x.strip() for x in result]
				# Remove duplicates
				result = list(set(result))
				return result
		return [None]

	@TextScraper._needs_download
	def superlative(self):

		if 'JJ' in self.pos():
			if self.tree.xpath(u'//div[@id="mw-content-text"]/p[@title="Trennungsmöglichkeiten am Zeilenumbruch"]'):
				content = self._normalize(self.tree.xpath(u'//div[@id="mw-content-text"]/p[@title="Trennungsmöglichkeiten am Zeilenumbruch"]')[0].getnext().text_content())
				result = re.findall('Superlativ[\d|\s]*: ([\w|\s]+)', content, re.U)
				result = [x.strip() for x in result]
				# Remove duplicates
				result = list(set(result))
				# Prepend "am " if necessary
				result = map(lambda x: 'am ' + x if not x.startswith('am ') else x, result)
				return result
		return [None]

register(WiktionaryDe)
