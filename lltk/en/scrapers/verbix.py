#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import html
import re

from ...scrapers import Verbix
from ...scraping import register

class VerbixEn(Verbix):

	def __init__(self, word):

		super(VerbixEn, self).__init__(word, 'en')

register('en', VerbixEn)
