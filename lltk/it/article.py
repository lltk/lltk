#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gender import *

def article(word):
	''' Try to find the correct articles for singular and plural using the pattern library. '''

	word, result = unicode(word), [None, None]
	wordgender = gender(word)
	if wordgender[0] in ['m', 'f']:
		try:
			_pattern = __import__('pattern.it', globals(), locals(), ['article'], -1)
		except ImportError:
			pass
		else:
			result[0] = _pattern.article(word, gender = wordgender, function = 'definite')
			if wordgender[0] == 'f':
				result[1] = 'le'
			else:
				if result[0] == 'il':
					result[1] = 'i'
				else:
					result[1] = 'gli'

	return result

if __name__ == "__main__":
	import sys
	if len(sys.argv) > 1:
		result = article(sys.argv[1].decode('utf-8'))
		if result[0]:
			print ', '.join(result)
