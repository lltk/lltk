#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import html
from itertools import groupby

def plural(word):
	''' Try to scrape the plural version from vandale.nl. '''
	''' Returns a list of possible plural forms or [''] if theres no plural. [None] if there's no answer. '''

	word = unicode(word)
	page = requests.get('http://www.vandale.nl/opzoeken?pattern=%s&lang=nn' % word)
	tree = html.fromstring(page.text)
	elements = tree.xpath('//span[@class="f0f"]/span[@class="f0j"]')
	if len(elements):
		elements = elements[0].getchildren()
		element = [element.text for element in elements]

		while element[0].isdigit():
			element = element[1:]
		singular = ''.join(element[0:element.index(' ')]).replace(u'\xb7', '')
		if not singular == word:
			return [None]

		if 'meervoud: ' in element:
			first = element.index('meervoud: ') + 1
			plurals = element[first:][:element[first:].index(')')]
			if ', ' in plurals:
				plurals.remove(', ')
			return plurals
		else:
			# This means there is no plural
			return ['']

	return [None]

if __name__ == "__main__":
	import sys
	if len(sys.argv) > 1:
		result = plural(sys.argv[1].decode('utf-8'))
		if result[0] == '':
			print '-'
		elif result[0]:
			print ', '.join(result)
