#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import html
from collections import Counter
from functools32 import lru_cache as caching

@caching(maxsize =8)
def gender(word):
	''' Try to scrape the correct gender for a given word from wordreference.com '''

	word = unicode(word)
	page = requests.get('http://www.wordreference.com/iten/%s' % word)
	tree = html.fromstring(page.text)
	if len(tree.xpath('//span[@class="noThreads"]')) or len(tree.xpath('//p[@id="noEntryFound"]')):
		# There are no result. This is most likely not a proper word
		return [None]
	elements = tree.xpath('//table[@class="WRD"]')
	if len(elements):
		elements = tree.xpath('//table[@class="WRD"]')[0]
		if len(elements):
			if '/iten/' in page.url:
				elements = elements.xpath('//td[@class="FrWrd"]/em[@class="POS2"]/text()')
			elif '/enit/' in page.url:
				elements = elements.xpath('//td[@class="ToWrd"]/em[@class="POS2"]/text()')
			else:
				return [None]

			element = [element[1:] for element in elements if element in ['nm', 'nf']]
			counter = Counter(element)
			if len(counter.most_common(1)):
				result = counter.most_common(1)[0][0]
				return [result]

	return [None]

if __name__ == "__main__":
	import sys
	if len(sys.argv) > 1:
		result = gender(sys.argv[1])
		if result[0]:
			print ', '.join(result)
