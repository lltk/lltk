#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import html
from functools32 import lru_cache as caching

@caching(maxsize =8)
def plural(word):
	''' Try to scrape the plural version from pons.eu. '''
	''' Returns a list of possible plural forms or [''] if theres no plural. [None] if there's no answer. '''

	word = unicode(word)
	page = requests.get('http://de.pons.eu/dict/search/results/?q=%s&l=dede' % word)
	tree = html.fromstring(page.text)

	if tree.xpath('//div[@class="error"]'):
		# We're going too fast. Too many queries in a short time
		from ..exceptions import GoingTooFast
		raise GoingTooFast('Too many queries in a short time. Hit the break.')

	elements = tree.xpath('//div[@rel="' + word + '"]//h2//span')
	mapto = {}
	if len(elements):
		for i in xrange(len(elements)):
			value = elements[i].attrib['class']
			if not mapto.has_key(value):
				mapto[value] = i
		if mapto.has_key('info'):
			# There is no plural for this word
			return ['']
		if mapto.has_key('flexion'):
			suffix = elements[mapto['flexion']].text
			if ',' in suffix:
				suffix = suffix.split(',')[1][:-1].strip()
			if suffix:
				if suffix.startswith('-'):
					return (word + suffix[1:]).split('/')
				else:
					return suffix.split('/')
			else:
				# Plural is the same as the singular
				return [word]

	return [None]

if __name__ == "__main__":
	import sys
	if len(sys.argv) > 1:
		result = plural(sys.argv[1].decode('utf-8'))
		if result[0] == '':
			print '-'
		elif result[0]:
			print ', '.join(result)
