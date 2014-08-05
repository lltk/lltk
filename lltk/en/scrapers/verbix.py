#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import html
import re

from lltk.scrapers import Verbix
from lltk.scraping import register

class VerbixEn(Verbix):

	def __init__(self, word):

		super(VerbixEn, self).__init__(word, 'en')

register(VerbixEn)
