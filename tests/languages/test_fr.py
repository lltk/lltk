#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pytest

pytestmark = [pytest.mark.fr, pytest.mark.slow]

class TestConfig:

	def test_import(self):
		''' Asserts that the module import works. '''

		import lltk.fr

	def test_conjugate(self):
		''' Asserts that conjugate() works. '''

		import lltk.fr
		import lltk.caching
		lltk.caching.enable('CouchDB')
		assert lltk.fr.conjugate('acheter', 'present') == [u"j' ach\xe8te", u'tu ach\xe8tes', u'il/elle ach\xe8te', u'ns achetons', u'vs achetez', u'ils/elles ach\xe8tent']
		assert lltk.fr.conjugate('acheter', 'past') == [u"j' achetais", u'tu achetais', u'il/elle achetait', u'ns achetions', u'vs achetiez', u'ils/elles achetaient']
		assert lltk.fr.conjugate('acheter', 'perfect') == [u"j' ai achet\xe9", u'tu as achet\xe9', u'il/elle a achet\xe9', u'ns avons achet\xe9', u'vs avez achet\xe9', u'ils/elles ont achet\xe9']
		assert lltk.fr.conjugate('acheter', 'future I') == [u"j' ach\xe8terai", u'tu ach\xe8teras', u'il/elle ach\xe8tera', u'ns ach\xe8terons', u'vs ach\xe8terez', u'ils/elles ach\xe8teront']
