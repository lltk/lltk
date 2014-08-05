#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import html
import re

from lltk.scraping import TextScraper
from lltk.locale import humanize

class Verbix(TextScraper):

	def __init__(self, word, language):

		super(Verbix, self).__init__(word)
		self.name = 'Verbix.com'
		self.url = 'http://www.verbix.com/webverbix/%s/%s.html' % (humanize(language), word)
		self.baseurl = 'http://www.verbix.com'
		self.language = language
		self.tenses = {'Present' : 'Present', 'Past' : 'Past', 'Perfect' : 'Perfect', 'Future I' : 'Future', 'Future II' : 'Future perfect', 'Pluperfect' : 'Pluperfect'}

	def _normalize(self, string):
		''' Returns a sanitized string. '''

		string = string.replace(u'\xa0', '')
		string = string.strip()
		return string

	@TextScraper._needs_download
	def _extract(self, identifier):
		''' Extracts data from conjugation table. '''

		conjugation = []
		if self.tree.xpath('//p/b[normalize-space(text()) = "' + identifier.decode('utf-8') + '"]'):
			p = self.tree.xpath('//p/b[normalize-space(text()) = "' + identifier.decode('utf-8') + '"]')[0].getparent()
			for font in p.iterfind('font'):
				text = self._normalize(font.text_content())
				next = font.getnext()
				text += ' ' + self._normalize(next.text_content())
				while True:
					next = next.getnext()
					if next.tag != 'span':
						break
					text += '/' + self._normalize(next.text_content())
				conjugation.append(text)
		return conjugation

	def conjugate(self, tense):
		''' Tries to conjugate a given verb using verbix.com.'''

		if self.tenses.has_key(tense):
			return self._extract(self.tenses[tense])
		elif self.tenses.has_key(tense.title()):
			return self._extract(self.tenses[tense.title()])
		return [None]
