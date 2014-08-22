#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pytest

class TestConfig:

	def test_import(self):
		''' Asserts that the module import works. '''

		import lltk.es

	def test_conjugate(self):
		''' Asserts that conjugate() works. '''

		import lltk.es
		import lltk.caching
		lltk.caching.enable('CouchDB')
		assert lltk.es.conjugate('comprar', 'present') == [u'yo compro', u't\xfa compras', u'\xe9l compra', u'nosotros compramos', u'vosotros compr\xe1is', u'ellos compran']
		assert lltk.es.conjugate('comprar', 'past') == [u'yo compraba', u't\xfa comprabas', u'\xe9l compraba', u'nosotros compr\xe1bamos', u'vosotros comprabais', u'ellos compraban']
		assert lltk.es.conjugate('comprar', 'perfect') == [u'yo he comprado', u't\xfa has comprado', u'\xe9l ha comprado', u'nosotros hemos comprado', u'vosotros hab\xe9is comprado', u'ellos han comprado']
		assert lltk.es.conjugate('comprar', 'future I') == [u'yo comprar\xe9', u't\xfa comprar\xe1s', u'\xe9l comprar\xe1', u'nosotros compraremos', u'vosotros comprar\xe9is', u'ellos comprar\xe1n']
