#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pytest

class TestConfig:

	def test_import(self):
		''' Asserts that the module import works. '''

		import lltk.caching

	def test_has_generic_cache(self):
		''' Asserts that GenericCache exists. '''

		import lltk.caching
		assert hasattr(lltk.caching, 'GenericCache')

	def test_has_no_cache(self):
		''' Asserts that NoCache exists. '''

		import lltk.caching
		assert hasattr(lltk.caching, 'NoCache')

	def test_disable(self):
		''' Asserts that disable() works. '''

		import lltk.caching
		lltk.caching.cache = None
		lltk.caching.disable()
		assert isinstance(lltk.caching.cache, lltk.caching.NoCache)
