#!/usr/bin/python
# -*- coding: UTF-8 -*-

__all__ = ['isempty']

def isempty(result):
	''' Finds out if a scraping result should be considered empty. '''

	if isinstance(result, list):
		for element in result:
			if isinstance(element, list):
				if not isempty(element):
					return False
			else:
				if element is not None:
					return False
	else:
		if result is not None:
			return False
	return True
