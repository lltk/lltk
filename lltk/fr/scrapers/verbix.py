#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import html
import re

from lltk.scrapers import Verbix
from lltk.scraping import register

class VerbixFr(Verbix):

	def __init__(self, word):

		super(VerbixFr, self).__init__(word, 'fr')
		self.tenses['Present'] = 'Présent'
		self.tenses['Past'] = 'Imparfait'
		self.tenses['Perfect'] = 'Passé composé'
		self.tenses['Pluperfect'] = 'Plus-que-parfait'
		self.tenses['Future I'] = 'Futur simple'
		self.tenses['Future II'] = 'Futur antérieur'

	def _normalize(self, string):
		''' Returns a sanitized string. '''

		string = super(VerbixFr, self)._normalize(string)
		string = string.replace('il; elle', 'il/elle')
		string = string.replace('ils; elles', 'ils/elles')
		string = string.strip()
		return string

register(VerbixFr)
