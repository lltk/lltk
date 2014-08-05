#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import html
import re

from lltk.scrapers import Verbix
from lltk.scraping import register

class VerbixDe(Verbix):

	def __init__(self, word):

		super(VerbixDe, self).__init__(word, 'de')
		self.tenses['Future I'] = 'Future I'
		self.tenses['Future II'] = 'Future II'

	def _normalize(self, string):
		''' Returns a sanitized string. '''

		string = super(VerbixDe, self)._normalize(string)
		string = string.replace('sie; Sie', 'sie')
		string = string.strip()
		return string

register(VerbixDe)
