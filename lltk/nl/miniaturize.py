#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import html
from itertools import groupby
from .. import helpers

def miniaturize(word):
	''' Try to scrape the miniaturized version from vandale.nl. '''
	''' Returns a list of possible forms or [''] if theres no miniature form. [None] if there's no answer. '''

	page = requests.get('http://www.vandale.nl/opzoeken?pattern=%s&lang=nn' % word)
	tree = html.fromstring(page.text)
	elements = tree.xpath('//span[@class="f0f"]/span[@class="f0j"]')[0].getchildren()
	element = [element.text for element in elements]

	while element[0].isdigit():
		element = element[1:]
	singular = ''.join(element[0:element.index(' ')]).replace(u'\xb7', '')
	if singular is not word:
		return [None]

	if 'verkleinwoord: ' in element:
		miniature = element[element.index('verkleinwoord: ') + 1]
		return [miniature]
	else:
		# This means there is no miniature form
		return ['']
	return [None]

if __name__ == "__main__":
	import sys
	if len(sys.argv) > 1:
		result = miniaturize(sys.argv[1].decode('utf-8'))
		if result[0] == '':
			print '-'
		elif result[0]:
			print ', '.join(result)
