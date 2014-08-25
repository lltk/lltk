#!/usr/bin/python
# -*- coding: UTF-8 -*-

__all__ = ['register', 'discover', 'scrape', 'Scrape', 'GenericScraper', 'DictScraper', 'TextScraper']

import requests
from lxml import html
from functools import wraps

import lltk.config as config

from lltk.caching import cached
from lltk.utils import isempty
from lltk.helpers import debug

scrapers = {}
discovered = {}

def register(scraper):
	''' Registers a scraper to make it available for the generic scraping interface. '''

	global scrapers
	language = scraper('').language
	if not language:
		raise Exception('No language specified for your scraper.')
	if scrapers.has_key(language):
		scrapers[language].append(scraper)
	else:
		scrapers[language] = [scraper]

def discover(language):
	''' Discovers all registered scrapers to be used for the generic scraping interface. '''

	debug('Discovering scrapers for \'%s\'...' % (language,))
	global scrapers, discovered
	for language in scrapers.iterkeys():
		discovered[language] = {}
		for scraper in scrapers[language]:
			blacklist = ['download', 'isdownloaded', 'getelements']
			methods = [method for method in dir(scraper) if method not in blacklist and not method.startswith('_') and callable(getattr(scraper, method))]
			for method in methods:
				if discovered[language].has_key(method):
					discovered[language][method].append(scraper)
				else:
					discovered[language][method] = [scraper]
	debug('%d scrapers with %d methods (overall) registered for \'%s\'.' % (len(scrapers[language]), len(discovered[language].keys()), language))

def scrape(language, method, word, *args, **kwargs):
	''' Uses custom scrapers and calls provided method. '''

	scraper = Scrape(language, word)
	if hasattr(scraper, method):
		function = getattr(scraper, method)
		if callable(function):
			return function(*args, **kwargs)
	else:
		raise NotImplementedError('The method ' + method + '() is not implemented so far.')

class Scrape(object):
	''' Provides a generic scraping interface to all available scrapers for a language. '''

	def __init__(self, language, word):

		global scrapers, discovered
		if scrapers and not discovered.has_key(language):
			discover(language)

		self.language = language
		self.word = word
		self.scrapers = scrapers
		if discovered.has_key(language):
			self.methods = discovered[self.language].keys()
		else:
			self.methods = []
		self.mode = 'default'
		self.source = None
		self.result = None
		self.results = []

		for method in self.methods:
			# Just make sure to make the special methods available for now.
			# A hook in __getattribute__ will take care of the rest.
			self.__dict__[method] = lambda *args, **kwargs: None

	def __getattribute__(self, name):

		try:
			methods = object.__getattribute__(self, 'methods')
		except AttributeError:
			pass
		else:
			if name in methods:
				f = lambda *args, **kwargs: self._scrape(name, *args, **kwargs)
				f.func_name = name
				f.func_doc = getattr(self.iterscrapers(name).next(), name).func_doc
				return f
		return super(Scrape, self).__getattribute__(name)

	def iterscrapers(self, method, mode = None):
		''' Iterates over all available scrapers. '''

		global discovered
		if discovered.has_key(self.language) and discovered[self.language].has_key(method):
			for Scraper in discovered[self.language][method]:
				yield Scraper

	def _scrape(self, method, *args, **kwargs):

		results = []

		for Scraper in self.iterscrapers(method):
			scraper = Scraper(self.word)
			function = getattr(scraper, method)
			delimiter = '-'
			key = delimiter.join(filter(None, [scraper.language, method, scraper.name.lower(), scraper.word.lower(), delimiter.join(args)]))
			key = key.strip()
			key = key.replace(' ', delimiter)
			from datetime import datetime
			extradata = {'type' : 'lltk-scraping-cache','language' : scraper.language, 'word' : scraper.word, 'method' : method, 'source' : scraper.name, 'url' : scraper.url, 'added' : datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}
			if config['caching']:
				function = cached(key, extradata)(function)
			result = function(*args, **kwargs)
			debug(u'%s: %s.%s(\'%s\') → %s (\'%s\')' % (scraper.name, scraper.language, method, scraper.word, result, scraper.url))
			if not isempty(result):
				self.source = scraper
				results.append(result)

		# Remove empty or incomplete answers
		self.results = self.clean(results)
		self.results = self.merge(self.results)

		if config['debug']:
			for i in xrange(len(self.results)):
				debug('%d) %s' % (i + 1, self.results[i]))

		if self.results:
			if (kwargs.has_key('mode') and kwargs['mode'] == 'all') or config['scraping-results-mode'] == 'all':
				# Return all results
				self.result = self.results
			else:
				# Return the first result (which is the best guess since the list is sorted by frequency of occurrence)
				self.result = self.results[0]
		else:
			self.result = [None]
		return self.result

	def merge(self, elements):
		''' Merges all scraping results to a list sorted by frequency of occurrence. '''

		from collections import Counter
		from lltk.utils import list2tuple, tuple2list
		# The list2tuple conversion is necessary because mutable objects (e.g. lists) are not hashable
		merged = tuple2list([value for value, count in Counter(list2tuple(list(elements))).most_common()])
		return merged

	def clean(self, elements):
		''' Removes empty or incomplete answers. '''

		cleanelements = []
		for i in xrange(len(elements)):
			if isempty(elements[i]):
				return []
			next = elements[i]
			if isinstance(elements[i], (list, tuple)):
				next = self.clean(elements[i])
			if next:
				cleanelements.append(elements[i])
		return cleanelements

class GenericScraper(object):
	''' Generic base class that all custom scrapers should be derived from. '''

	def __init__(self, word):

		self.word = unicode(word)
		self.name = 'Unknown'
		self.license = None
		self.url = ''
		self.baseurl = ''
		self.language = ''
		self.page = None
		self.tree = None

	def __str__(self):
		return '%s (%s): %s' % (self.name, self.baseurl, self.url)

	@classmethod
	def _needs_download(self, f):
		''' Decorator used to make sure that the downloading happens prior to running the task. '''

		@wraps(f)
		def wrapper(self, *args, **kwargs):
			if not self.isdownloaded():
				self.download()
			return f(self, *args, **kwargs)
		return wrapper

	def download(self):
		''' Downloads HTML from url. '''

		self.page = requests.get(self.url)
		self.tree = html.fromstring(self.page.text)

	def pos(self):
		''' Tries to decide about the part of speech. '''
		return []

	def isdownloaded(self):
		''' Returns True if download() has already been called. '''
		return bool(self.page)

	def isnoun(self):
		''' Tries to decide whether a given word is a noun. '''

		if 'NN' in self.pos():
			return True
		return False

	def isverb(self):
		''' Tries to decide whether a given word is a verb. '''

		if 'VB' in self.pos():
			return True
		return False

	def isadjective(self):
		''' Tries to decide whether a given word is an adjective. '''

		if 'JJ' in self.pos():
			return True
		return False

	def hasplural(self):
		''' Tries to find out whether a given noun has a plural form. '''

		plural = self.plural()
		if plural == ['']:
			return False
		if plural[0]:
			return True
		return None

class DictScraper(GenericScraper):
	''' DictScraper should be used for dictionary-like sites (more than one result). '''

	def __init__(self, word):

		super(DictScraper, self).__init__(word)
		self.elements = None

	@classmethod
	def _needs_elements(self, f):
		''' Decorator used to make sure that there are elements prior to running the task. '''

		@wraps(f)
		def wrapper(self, *args, **kwargs):
			if self.elements == None:
				self.getelements()
			return f(self, *args, **kwargs)
		return wrapper

	def _first(self, tag):
		''' Returns the first element with required POS-tag. '''

		self.getelements()
		for element in self.elements:
			if tag in self.pos(element):
				return element
		return None

class TextScraper(GenericScraper):
	''' TextScraper should be used for text-like sites (one result) such as Wiktionary. '''

	def __init__(self, word):
		super(TextScraper, self).__init__(word)
