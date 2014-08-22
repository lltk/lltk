#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pytest

class TestConfig:

	def test_import(self):
		''' Asserts that the module import works. '''

		import lltk.it

	def test_pos(self):
		''' Asserts that pos() works. '''

		import lltk.it
		import lltk.caching
		lltk.caching.enable('CouchDB')
		assert lltk.it.pos(u'gatto') == [u'NN']
		assert lltk.it.pos(u'uscire') == [u'VB']
		assert lltk.it.pos(u'lento') == [u'JJ']

	def test_articles(self):
		''' Asserts that articles() works. '''

		import lltk.it
		import lltk.caching
		lltk.caching.enable('CouchDB')
		assert lltk.it.articles(u'cane') == [[u'il'], [u'i']]
		assert lltk.it.articles(u'città') == [[u'la'], [u'le']]
		assert lltk.it.articles(u'aeroporto') == [[u'l\''], [u'gli']]

	def test_plural(self):
		''' Asserts that plural() works. '''

		import lltk.it
		import lltk.caching
		lltk.caching.enable('CouchDB')
		assert lltk.it.plural(u'cane') == [u'cani']
		assert lltk.it.plural(u'gatto') == [u'gatti']
		assert lltk.it.plural(u'regina') == [u'regine']

	def test_gender(self):
		''' Asserts that gender() works. '''

		import lltk.it
		import lltk.caching
		lltk.caching.enable('CouchDB')
		assert lltk.it.gender(u'bambino') == u'm'
		assert lltk.it.gender(u'nonna') == u'f'
		assert lltk.it.gender(u'elefante') == u'm'

	def test_conjugate(self):
		''' Asserts that conjugate() works. '''

		import lltk.it
		import lltk.caching
		lltk.caching.enable('CouchDB')
		assert lltk.it.conjugate('comprare', 'present') == [u'io compro', u'tu compri', u'lui compra', u'noi compriamo', u'voi comprate', u'loro comprano']
		assert lltk.it.conjugate('comprare', 'past') == [u'io compravo', u'tu compravi', u'lui comprava', u'noi compravamo', u'voi compravate', u'loro compravano']
		assert lltk.it.conjugate('comprare', 'perfect') == [u'io ho comprato', u'tu hai comprato', u'lui ha comprato', u'noi abbiamo comprato', u'voi avete comprato', u'loro hanno comprato']
		assert lltk.it.conjugate('comprare', 'future I') == [u'io comprer\xf2', u'tu comprerai', u'lui comprer\xe0', u'noi compreremo', u'voi comprerete', u'loro compreranno']
