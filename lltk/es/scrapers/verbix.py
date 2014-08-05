#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import html
import re

from lltk.scrapers import Verbix
from lltk.scraping import register

class VerbixEs(Verbix):

	def __init__(self, word):

		super(VerbixEs, self).__init__(word, 'es')
		self.tenses['Present'] = 'Presente'
		self.tenses['Past'] = 'Pretérito imperfecto'
		self.tenses['Perfect'] = 'Pretérito perfecto compuesto'
		self.tenses['Pluperfect'] = 'Pretérito pluscuamperfecto'
		self.tenses['Future I'] = 'Futuro'
		self.tenses['Future II'] = 'Futuro perfecto'

register(VerbixEs)
