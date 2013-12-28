#!/usr/bin/python
# -*- coding: UTF-8 -*-

__all__ = ['scrapers', 'scrape', 'pos', 'articles', 'plural', 'ipa', 'conjugate', 'gender', 'miniaturize']

import scrapers

ISO639_1 = 'nl'

def scrape(word, method, mode = None):
	''' Uses custom scrapers and calls provided method (with provided scraping mode). '''
	# @TODO: Introduce different scraping modes

	from ..scraping import Scrape

	scrape = Scrape(ISO639_1, word)
	if hasattr(scrape, method):
		return eval('scrape.' + method + '()')
	raise NotImplementedError

def pos(word):
	''' Returns a list of possible POS-tags (part-of-speech) for a given word. '''
	return scrape(word, 'pos')

def articles(word):
	''' Returns the articles (singular and plural) for a given noun. '''
	return scrape(word, 'articles')

def plural(word):
	''' Returns the plural version for a given noun. '''
	return scrape(word, 'plural')

def ipa(word):
	''' Returns the International Phonetic Alphabet (IPA) writing for a given word. '''
	return scrape(word, 'ipa')

def conjugate(word):
	''' Returns the conjugation of a given verb. '''
	return scrape(word, 'conjugate')

def gender(word):
	''' Returns the gender for a given word. '''
	return scrape(word, 'gender')

def miniaturize(word):
	''' Returns the miniaturized version for a given word. '''
	return scrape(word, 'miniaturize')
