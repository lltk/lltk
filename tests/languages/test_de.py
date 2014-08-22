#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pytest

class TestConfig:

	def test_import(self):
		''' Asserts that the module import works. '''

		import lltk.de

	def test_pos(self):
		''' Asserts that pos() works. '''

		import lltk.de
		import lltk.caching
		lltk.caching.enable('CouchDB')
		assert lltk.de.pos(u'Auto') == [u'NN']
		assert lltk.de.pos(u'kaufen') == [u'VB']
		assert lltk.de.pos(u'heiß') == [u'JJ']

	def test_articles(self):
		''' Asserts that articles() works. '''

		import lltk.de
		import lltk.caching
		lltk.caching.enable('CouchDB')
		assert lltk.de.articles(u'Mann') == [[u'der'], [u'die']]
		assert lltk.de.articles(u'Frau') == [[u'die'], [u'die']]
		assert lltk.de.articles(u'Kind') == [[u'das'], [u'die']]


	def test_plural(self):
		''' Asserts that plural() works. '''

		import lltk.de
		import lltk.caching
		lltk.caching.enable('CouchDB')
		assert lltk.de.plural(u'Hund') == [u'Hunde']
		assert lltk.de.plural(u'Katze') == [u'Katzen']
		assert lltk.de.plural(u'Maus') == [u'M\xe4use']

	def test_gender(self):
		''' Asserts that gender() works. '''

		import lltk.de
		import lltk.caching
		lltk.caching.enable('CouchDB')
		assert lltk.de.gender(u'Mann') == u'm'
		assert lltk.de.gender(u'Frau') == u'f'
		assert lltk.de.gender(u'Spiel') == u'n'

	def test_conjugate(self):
		''' Asserts that conjugate() works. '''

		import lltk.de
		import lltk.caching
		lltk.caching.enable('CouchDB')
		assert lltk.de.conjugate('bauen', 'present') == [u'ich baue', u'du baust', u'er baut', u'wir bauen', u'ihr baut', u'sie bauen']
		assert lltk.de.conjugate('bauen', 'past') == [u'ich baute', u'du bautest', u'er baute', u'wir bauten', u'ihr bautet', u'sie bauten']
		assert lltk.de.conjugate('bauen', 'perfect') == [u'ich habe gebaut', u'du hast gebaut', u'er hat gebaut', u'wir haben gebaut', u'ihr habt gebaut', u'sie haben gebaut']
		assert lltk.de.conjugate('bauen', 'future I') == [u'ich werde bauen', u'du wirst bauen', u'er wird bauen', u'wir werden bauen', u'ihr werdet bauen', u'sie werden bauen']

	def test_comparative(self):
		''' Asserts that comparative() works. '''

		import lltk.de
		import lltk.caching
		lltk.caching.enable('CouchDB')
		assert lltk.de.comparative(u'schnell') == [u'schneller']
		assert lltk.de.comparative(u'hoch') == [u'höher']
		assert lltk.de.comparative(u'gut') == [u'besser']

	def test_superlative(self):
		''' Asserts that superlative() works. '''

		import lltk.de
		import lltk.caching
		lltk.caching.enable('CouchDB')
		assert lltk.de.superlative(u'weit') == [u'am weitesten']
		assert lltk.de.superlative(u'langsam') == [u'am langsamsten']
		assert lltk.de.superlative(u'gut') == [u'am besten']
