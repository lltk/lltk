#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pytest

class TestConfig:

	def test_import(self):
		''' Asserts that the module import works. '''

		import lltk.nl

	def test_pos(self):
		''' Asserts that pos() works. '''

		import lltk.nl
		import lltk.caching
		lltk.caching.enable('CouchDB')
		assert lltk.nl.pos(u'auto') == [u'NN']
		assert lltk.nl.pos(u'kopen') == [u'VB']
		assert lltk.nl.pos(u'heet') == [u'JJ']

	def test_articles(self):
		''' Asserts that articles() works. '''

		import lltk.nl
		import lltk.caching
		lltk.caching.enable('CouchDB')
		assert lltk.nl.articles(u'man') == [[u'de'], [u'de']]
		assert lltk.nl.articles(u'vrouw') == [[u'de'], [u'de']]
		assert lltk.nl.articles(u'kind') == [[u'het'], [u'de']]


	def test_plural(self):
		''' Asserts that plural() works. '''

		import lltk.nl
		import lltk.caching
		lltk.caching.enable('CouchDB')
		assert lltk.nl.plural(u'hond') == [u'honden']
		assert lltk.nl.plural(u'kat') == [u'katten']
		assert lltk.nl.plural(u'muis') == [u'muizen']

	def test_gender(self):
		''' Asserts that gender() works. '''

		pass

	def test_conjugate(self):
		''' Asserts that conjugate() works. '''

		import lltk.nl
		import lltk.caching
		lltk.caching.enable('CouchDB')
		assert lltk.nl.conjugate('bouwen', 'present') == [u'ik bouw', u'jij bouwt', u'hij bouwt', u'wij bouwen', u'jullie bouwen', u'zij bouwen']
		assert lltk.nl.conjugate('bouwen', 'past') == [u'ik bouwde', u'jij bouwde', u'hij bouwde', u'wij bouwden', u'jullie bouwden', u'zij bouwden']
		assert lltk.nl.conjugate('bouwen', 'perfect') == [u'ik heb gebouwd', u'jij hebt gebouwd', u'hij heeft gebouwd', u'wij hebben gebouwd', u'jullie hebben gebouwd', u'zij hebben gebouwd']
		assert lltk.nl.conjugate('bouwen', 'future I') == [u'ik zal bouwen', u'jij zult bouwen', u'hij zal bouwen', u'wij zullen bouwen', u'jullie zullen bouwen', u'zij zullen bouwen']

	def test_miniaturize(self):
		''' Asserts that miniaturize() works. '''

		import lltk.nl
		import lltk.caching
		lltk.caching.enable('CouchDB')
		assert lltk.nl.miniaturize(u'man') == [u'mannetje']
		assert lltk.nl.miniaturize(u'auto') == [u'autootje']
		assert lltk.nl.miniaturize(u'bal') == [u'balletje']
