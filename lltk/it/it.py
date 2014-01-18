#!/usr/bin/python
# -*- coding: UTF-8 -*-

__all__ = ['scrapers', 'scrape', 'pos', 'articles', 'plural', 'ipa', 'gender']

import scrapers
from ..scraping import scrape
from ..decorators import language

ISO639_1 = 'it'
scrape = language(ISO639_1)(scrape)

def pos(word):
	''' Returns a list of possible POS-tags (part-of-speech) for a given word. '''
	return scrape('pos', word)

def ipa(word):
	''' Returns the International Phonetic Alphabet (IPA) writing for a given word. '''
	return scrape('ipa', word)

def gender(word):
	''' Returns the gender for a given word. '''
	return scrape('gender', word)
