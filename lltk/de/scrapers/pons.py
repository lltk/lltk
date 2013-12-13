#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import html

from ...scraping import Scraper

class PonsDe(Scraper):

	def __init__(self, word):
		super(PonsDe, self).__init__( word)
		self.name = 'Pons.eu'
		self.url = 'http://de.pons.eu/dict/search/results/?q=%s&l=dede' % self.word
		self.baseurl = 'http://de.pons.eu'
		self.language = 'de'

	def download(self):
		super(PonsDe, self).download()
		if self.tree.xpath('//div[@class="error"]'):
			# We're going too fast. Too many queries in a short time
			from ..exceptions import GoingTooFast
			raise GoingTooFast('Too many queries in a short time. Hit the break.')

	@Scraper.needs_download
	def article(self):
		''' Try to scrape the correct articles for singular and plural from de.pons.eu. '''

		elements = self.tree.xpath('//div[@rel="' + self.word + '"]//h2//span')
		mapto, result = {}, [None, None]
		if len(elements):
			for i in xrange(len(elements)):
				mapto[elements[i].attrib['class']] = i
			if mapto.has_key('info'):
				# There is no plural for this word
				result[1] = ''
			else:
				result[1] = 'die'
			if mapto.has_key('genus') and elements[mapto['genus']].text.strip() in ['der', 'die', 'das']:
				result[0] = elements[mapto['genus']].text.strip()
			else:
				result[0] = None
		return result

	@Scraper.needs_download
	def plural(self):
		''' Try to scrape the plural version from pons.eu. '''

		elements = self.tree.xpath('//div[@rel="' + self.word + '"]//h2//span')
		mapto = {}
		if len(elements):
			for i in xrange(len(elements)):
				value = elements[i].attrib['class']
				if not mapto.has_key(value):
					mapto[value] = i
			if mapto.has_key('info'):
				# There is no plural for this word
				return ['']
			if mapto.has_key('flexion'):
				suffix = elements[mapto['flexion']].text
				if ',' in suffix:
					suffix = suffix.split(',')[1][:-1].strip()
				if suffix:
					if suffix.startswith('-'):
						return (self.word + suffix[1:]).split('/')
					else:
						return suffix.split('/')
				else:
					# Plural is the same as the singular
					return [self.word]
		return [None]
