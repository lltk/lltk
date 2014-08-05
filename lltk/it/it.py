#!/usr/bin/python
# -*- coding: UTF-8 -*-

__all__ = ['scrapers', 'scrape', 'pos', 'articles', 'plural', 'ipa', 'conjugate', 'gender']

import scrapers
from lltk.scraping import scrape
from lltk.decorators import language

ISO639_1 = 'it'
scrape = language(ISO639_1)(scrape)

def pos(word):
	''' Returns a list of possible POS-tags (part-of-speech) for a given word. '''
	return scrape('pos', word)

def articles(word):
	''' Returns the articles (singular and plural) for a given noun. '''

	from pattern.it import article

	result = [[None], [None]]
	genus = gender(word) or 'f'
	result[0] = [article(word, function = 'definite', gender = genus)]
	result[1] = [article(plural(word)[0], function = 'definite', gender = (genus, 'p'))]
	return result

def plural(word):
	''' Returns the plural version for a given noun. '''

	from pattern.it import pluralize
	return [pluralize(word, pos = 'NN')]

def ipa(word):
	''' Returns the International Phonetic Alphabet (IPA) writing for a given word. '''
	return scrape('ipa', word)

def conjugate(word, tense):
	''' Returns the conjugation of a given verb. '''
	return scrape('conjugate', word, tense)

def gender(word):
	''' Returns the gender for a given word. '''
	return scrape('gender', word)
