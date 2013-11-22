#!/usr/bin/python
# -*- coding: UTF-8 -*-

def article(word = None):
	''' Get the correct articles for singular and plural. That's an easy one. '''
	return ['the', 'the']

if __name__ == "__main__":
	import sys
	if len(sys.argv) > 1:
		result = article(sys.argv[1].decode('utf-8'))
		if result[0]:
			print ', '.join(result)
