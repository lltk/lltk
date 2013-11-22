#!/usr/bin/python
# -*- coding: UTF-8 -*-

from pattern.it import pluralize

def plural(word):
	''' Try to find the correct plural version using Pattern (CLiPS) library. '''
	''' Returns a list of possible plural forms. '''

	word = unicode(word)
	pluralword = pluralize(word)

	# Do some minor adjustments to avoid common mistakes
	# @TODO: Lookup if that's all correct

	if pluralword.endswith('che'):
		pluralword = pluralword[:-3] + 'cche'
	elif pluralword.endswith('cci'):
		pluralword = pluralword[:-3] + 'cchi'
	elif pluralword.endswith('gi') and not pluralword.endswith('ggi') and not pluralword.endswith('agi') and not pluralword.endswith('egi') and not pluralword.endswith('igi') and not pluralword.endswith('ogi') and not pluralword.endswith('ugi'):
		pluralword = pluralword[:-2] + 'ghi'
	elif pluralword.endswith('ii'):
		pluralword = pluralword[:-1]

	return [pluralword]

if __name__ == "__main__":
	import sys
	if len(sys.argv) > 1:
		result = plural(sys.argv[1].decode('utf-8'))
		if result[0] == '':
			print '-'
		elif result[0]:
			print ', '.join(result)
