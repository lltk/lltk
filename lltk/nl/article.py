#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import html
from itertools import groupby
from functools32 import lru_cache as caching

@caching(maxsize =8)
def article(word):
	''' Try to scrape the correct articles for singular and plural from vandale.nl. '''
	''' Returns a list of articles in format [singluar, plural]. If there's no singular/plural form the string will be empty. None-list if there's no answer. '''

	word, result = unicode(word), [None, None]
	page = requests.get('http://www.vandale.nl/opzoeken?pattern=%s&lang=nn' % word)
	tree = html.fromstring(page.text)
	elements = tree.xpath('//span[@class="f0f"]/span[@class="f0j"]')
	if len(elements):
		elements = elements[0].getchildren()

		if not elements:
			from sys import exit
			from .. import helpers
			vars = globals().copy()
			vars.update(locals())
			print 'Something went wrong. Opening debug console...'
			helpers.interactiveconsole(vars)
			print 'Quitting.'
			exit(1)


		element = [element.text for element in elements]

		while element[0].isdigit():
			element = element[1:]
		singular = ''.join(element[0:element.index(' ')]).replace(u'\xb7', '')
		if not singular == word:
			return [None, None]

		element = [singular] + element[element.index(' ') + 1:]
		if element[2] in ['de', 'het', 'de/het', 'het/de']:
			result[0] = element[2]
		else:
			# No article specified. Let's say it's 'de'
			result[0] = 'de'

		if not 'meervoud: ' in element:
			# This means there is no plural
			result[1] = ''
		else:
			result[1] = 'de'

	return result

if __name__ == "__main__":
	import sys
	if len(sys.argv) > 1:
		result = article(sys.argv[1].decode('utf-8'))
		if result[0]:
			print ', '.join(result)
