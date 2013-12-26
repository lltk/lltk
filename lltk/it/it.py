#!/usr/bin/python
# -*- coding: UTF-8 -*-

__all__ = ['scrapers', 'scrape', 'pos', 'ipa', 'gender']

import scrapers

ISO639_1 = 'it'

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

def ipa(word):
	''' Returns the International Phonetic Alphabet (IPA) writing for a given word. '''
	return scrape(word, 'ipa')

def gender(word):
	''' Returns the gender for a given word. '''
	return scrape(word, 'gender')
