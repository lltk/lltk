#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys

class Config(object):
	''' Config class providing the configuration interface. '''

	def __init__(self):

		import lltk, os
		self.settings = {}
		self.settings['module-path'] = os.path.dirname(os.path.abspath(lltk.__file__))
		self.default()

	def __getitem__(self, key):

		if self.settings.has_key(key):
			return self.settings[key]
		return None

	def __setitem__(self, key, value):
		self.settings[key] = value

	def exists(self, key):
		''' Checks if a configuration option exists. '''
		return self.settings.has_key(key)

	def default(self):
		''' Loads the default configuration. '''

		return self.load(self.settings['module-path'] + '/config/default.config')

	def show(self):
		''' Returns a dictionary containing the current configuration. '''

		return self.settings

	def load(self, filename, replace = False):
		''' Loads a configuration file (JSON). '''

		import os, json, re
		if os.path.exists(filename):
			f = open(filename, 'r')
			content = f.read()
			content = re.sub('[\t ]*?[#].*?\n', '', content)
			try:
				settings = json.loads(content)
			except ValueError:
				# This means that the configuration file is not a valid JSON document
				from lltk.exceptions import ConfigurationError
				raise ConfigurationError('\'' + filename + '\' is not a valid JSON document.')
			f.close()
			if replace:
				self.settings = settings
			else:
				self.settings.update(settings)
		else:
			lltkfilename = self.settings['module-path'] + '/' + self.settings['lltk-config-path'] + filename
			if os.path.exists(lltkfilename):
				# This means that filename was provided relative to the lltk module path
				return self.load(lltkfilename)
			from lltk.exceptions import ConfigurationError
			raise ConfigurationError('\'' + filename + '\' seems to be non-existent.')

	def save(self, filename):
		''' Saves the current configuration to file 'filename' (JSON). '''

		import json
		f = open(filename, 'w')
		json.dump(self.settings, f, indent = 4)
		f.close()

sys.modules[__name__] = Config()
