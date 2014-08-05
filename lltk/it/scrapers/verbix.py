#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import html
import re

from lltk.scrapers import Verbix
from lltk.scraping import register

class VerbixIt(Verbix):

	def __init__(self, word):

		super(VerbixIt, self).__init__(word, 'it')
		self.tenses['Present'] = 'Presente'
		self.tenses['Past'] = 'Imperfetto'
		self.tenses['Perfect'] = 'Passato prossimo'
		self.tenses['Pluperfect'] = 'Trapassato prossimo'
		self.tenses['Future I'] = 'Futuro'
		self.tenses['Future II'] = 'Futuro anteriore'

register(VerbixIt)
