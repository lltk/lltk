#!/usr/bin/python
# -*- coding: UTF-8 -*-

__all__ = ['isempty', 'method2pos']

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

def method2pos(method):
	''' Returns a list of valid POS-tags for a given method. '''

	if method in ('articles', 'plural', 'miniaturize', 'gender'):
		pos = ['NN']
	elif method in ('conjugate',):
		pos = ['VB']
	elif method in ('comparative, superlative'):
		pos = ['JJ']
	else:
		pos = ['*']
	return pos

def list2tuple(elements):
	''' '''

	for i in xrange(len(elements)):
		if isinstance(elements[i], list):
			elements[i] = list2tuple(elements[i])
	return tuple(elements)

def tuple2list(elements):

	elements = list(elements)
	for i in xrange(len(elements)):
		if isinstance(elements[i], tuple):
			elements[i] = tuple2list(elements[i])
	return elements
