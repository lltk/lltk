#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pytest
import os

pytestmark = [pytest.mark.config]

class TestConfig:

	def test_import(self):
		''' Asserts that the module import works. '''

		import lltk.config

	def test_find_default_config(self):
		''' Asserts that the default configuration file exists. '''

		path = 'lltk/config/default.config'
		if not os.path.exists(path):
			pytest.fail('Default config file (\'' + path + '\') not found.')

	def test_load_default_config(self):
		''' Asserts that the default configuration can be loaded (and is valid JSON). '''

		import lltk.config
		lltk.config.default()
		config = lltk.config.show()
		assert config != dict()

	def test_is_module_path_set(self):
		''' Asserts that config['module-path'] is set. '''

		import lltk.config
		assert lltk.config.exists('module-path') == True

	def test_exists(self):
		''' Asserts that exists() works. '''

		import lltk.config
		assert type(lltk.config.exists('**********')) == bool
		assert lltk.config.exists('**********') == False

	def test_access_unset_configuration_option(self):
		''' Asserts that unset configuration values can be accessed. '''

		import lltk.config
		if not lltk.config.exists('**********'):
			assert lltk.config['**********'] == None

	def test_save(self):
		''' Asserts that save() works. '''
		pass
