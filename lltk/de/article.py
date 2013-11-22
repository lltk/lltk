#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import html
from functools32 import lru_cache as caching

@caching(maxsize =8)
def article(word):
	''' Try to scrape the correct articles for singular and plural from pons.eu. '''

	word, result = unicode(word), [None, None]
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
			mapto[elements[i].attrib['class']] = i
		if mapto.has_key('info'):
			# There is no plural for this word
			result[1] = ''
		else:
			result[1] = 'die'
		if mapto.has_key('genus') and elements[mapto['genus']].text.strip() in ['der', 'die', 'das']:
			result[0] = elements[mapto['genus']].text.strip()
		else:
			result[0] = None

	return result

if __name__ == "__main__":
	import sys
	if len(sys.argv) > 1:
		result = article(sys.argv[1].decode('utf-8'))
		if result[0]:
			print ', '.join(result)
