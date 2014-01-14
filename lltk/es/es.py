#!/usr/bin/python
# -*- coding: UTF-8 -*-

__all__ = ['scrapers', 'scrape']

import scrapers

ISO639_1 = 'es'

def scrape(word, method, mode = None):
	''' Uses custom scrapers and calls provided method (with provided scraping mode). '''
	# @TODO: Introduce different scraping modes

	from ..scraping import Scrape

	scrape = Scrape(ISO639_1, word)
	if hasattr(scrape, method):
		return eval('scrape.' + method + '()')
	raise NotImplementedError
