#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import html
import re

from ...scraping import TextScraper, register

class MijnWoordenBoekNl(TextScraper):

	def __init__(self, word):

		super(MijnWoordenBoekNl, self).__init__(word)
		self.name = 'Mijnwoordenboek.nl'
		self.url = 'http://www.mijnwoordenboek.nl/vertalen.php?s1=&s2=NL+%%3E+EN&s3=NL+%%3E+EN&woord=%s' % self.word
		self.baseurl = 'http://www.mijnwoordenboek.nl'
		self.language = 'nl'

	def _normalize(self, string):

		string = string.replace(u'\xa0', '')
		return string

	@TextScraper._needs_download
	def pos(self):
		''' Try to decide about the part of speech. '''

		tags = []
		if self.tree.xpath('//div[@class="grad733100"]/h2[@class="inline"]//text()'):
			info = self.tree.xpath('//div[@class="grad733100"]/h2[@class="inline"]')[0].text_content()
			info = info.strip('I ')
			if info.startswith(('de', 'het')):
				tags.append('NN')
			if not info.startswith(('de', 'het')) and info.endswith('en'):
				tags.append('VB')
			if not info.startswith(('de', 'het')) and not info.endswith('en'):
				tags.append('JJ')
		return tags

	@TextScraper._needs_download
	def ipa(self):

		if self.tree.xpath('//div[@class="grad733100"]/table'):
			info = self.tree.xpath('//div[@class="grad733100"]/table')[0].text_content().encode('latin-1')
			if re.search('Uitspraak:.+\[(.+)\]', info, re.U):
				result = re.findall('Uitspraak:.+\[(.+)\]', info, re.U)[0]
				result = result.decode('utf-8').strip('/')
				return [result]
		return [None]

	@TextScraper._needs_download
	def articles(self):

		result = [None, None]
		if 'NN' in self.pos():
			content = self.tree.xpath('//div[@class="grad733100"]/h2[@class="inline"]')[0].text_content()
			info, content = '', content.strip('I ')
			article, word = content.split(' ')[0].strip(), ''.join(content.split(' ')[1:]).strip()
			if self.tree.xpath('//div[@class="grad733100"]/table'):
				info = self.tree.xpath('//div[@class="grad733100"]/table')[0].text_content().encode('latin-1')
			if article in ('de', 'het'):
				result[0] = article
			if '(meerv.)' in info:
				# There is a plural form
				result[1] = 'de'
			else:
				# There is no plural form
				result[1] = ''
		return result

	@TextScraper._needs_download
	def plural(self):

		if 'NN' in self.pos():
			content = self.tree.xpath('//div[@class="grad733100"]/h2[@class="inline"]')[0].text_content()
			info, content = '', content.strip('I ')
			article, word = content.split(' ')[0], ''.join(content.split(' ')[1:])
			if self.tree.xpath('//div[@class="grad733100"]/table'):
				info = self.tree.xpath('//div[@class="grad733100"]/table')[0].text_content().encode('latin-1')
			if re.search('-(\w+) \(meerv.\)', info, re.U):
				# Suffix is provided
				suffix = re.findall('-(\w+) \(meerv.\)', info, re.U)[0].strip()
				return [word + suffix]
			elif re.search('([\w|\s]+) \(meerv.\)', info, re.U):
				# Plural form is provided
				result = re.findall('([\w|\s]+) \(meerv.\)', info, re.U)[0].strip()
				return [result]
			else:
				# There is no plural
				return ['']
		return [None]

	@TextScraper._needs_download
	def conjugate(self):

		conjugation = [None, None, None]
		if 'VB' in self.pos():
			if self.tree.xpath('//div[@class="grad733100"]/table'):
				info = self._normalize(self.tree.xpath('//div[@class="grad733100"]/table')[0].text_content()).encode('latin-1')
				print info
				if re.search('([\w|\s]+) \(verl\.tijd \) ([\w|\s]+) \(volt\.deelw\.\)', info, re.U):
					conjugation[0] = self.word
					conjugation[1], conjugation[2] = re.findall('([\w|\s]+) \(verl\.tijd \) ([\w|\s]+) \(volt\.deelw\.\)', info, re.U)[0]
					conjugation[2] = conjugation[2].replace(' of ', '/')
					conjugation = [x.strip() for x in conjugation]
					conjugation = [x.split('/') for x in conjugation]
		return conjugation

register('nl', MijnWoordenBoekNl)
