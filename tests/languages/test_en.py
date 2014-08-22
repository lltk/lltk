#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pytest

class TestConfig:

	def test_import(self):
		''' Asserts that the module import works. '''

		import lltk.en

	def test_conjugate(self):
		''' Asserts that conjugate() works. '''

		import lltk.en
		import lltk.caching
		lltk.caching.enable('CouchDB')
		assert lltk.en.conjugate('build', 'present') == [u'I build', u'you build', u'he builds', u'we build', u'you build', u'they build']
		assert lltk.en.conjugate('build', 'past') == [u'I built', u'you built', u'he built', u'we built', u'you built', u'they built']
		assert lltk.en.conjugate('build', 'perfect') == [u'I have built', u'you have built', u'he has built', u'we have built', u'you have built', u'they have built']
		assert lltk.en.conjugate('build', 'future I') == [u'I will build', u'you will build', u'he will build', u'we will build', u'you will build', u'they will build']
