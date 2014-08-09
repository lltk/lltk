#!/usr/bin/python
# -*- coding: UTF-8 -*-

__all__ = ['register', 'enable', 'disable', 'get', 'put', 'exists', 'cached', 'Cache']

from functools import wraps

caches = {}

def register(cache):
	''' Registers a cache. '''

	global caches
	name = cache().name
	if not caches.has_key(name):
		caches[name] = cache

def enable(identifier = None, *args, **kwargs):
	''' Enables a specific cache for the current session. Remember that is has to be registered. '''

	global cache
	if not identifier:
		if caches:
			cache = caches[caches.keys()[0]](*args, **kwargs)
	elif caches.has_key(identifier):
		cache = caches[identifier](*args, **kwargs)

def disable():
	''' Disables the cache for the current session. '''

	global cache
	cache = NoCache()

def exists(key):
	''' Checks if a document is cached. '''
	return cache.exists(key)

def get(key):
	''' Retrieves a document from the the currently activated cache (by unique identifier). '''
	return cache.get(key)

def put(key, value, extradata = {}):
	''' Caches a document using the currently activated cache. '''
	return cache.put(key, value, extradata)

def delete(key):
	''' Remove a document from the cache (by unique identifier). '''
	return cache.delete(key)

def commit():
	''' Ensures that all changes are committed to disc. '''
	return cache.commit()

def cached(key = None, extradata = {}):
	''' Decorator used for caching. '''

	def decorator(f):

		@wraps(f)
		def wrapper(*args, **kwargs):

			uid = key
			if not uid:
				from hashlib import md5
				arguments = list(args) + [(a, kwargs[a]) for a in sorted(kwargs.keys())]
				uid = md5(str(arguments)).hexdigest()
			if exists(uid):
				return get(uid)
			else:
				result = f(*args, **kwargs)
				put(uid, result, extradata)
				return result
		return wrapper
	return decorator

class GenericCache(object):
	''' Generic cache class that all custom caches should be derived from. '''

	def __init__(self, *args, **kwargs):

		self.name = 'Unkown'
		self.server = None
		self.port = None
		self.user = None
		self.database = None
		self.filename = None
		if kwargs.has_key('server'):
			self.server = kwargs['server']
		if kwargs.has_key('port'):
			self.port = kwargs['port']
		if kwargs.has_key('user'):
			self.user = kwargs['user']
		if kwargs.has_key('database'):
			self.database = kwargs['database']
		if kwargs.has_key('filename'):
			self.filename = kwargs['filename']
		pass

	def __del__(self):
		self.commit()

	def setup(self):
		''' Runs the initial setup for the cache. '''
		pass

	def exists(self, key):
		''' Checks if a document is cached. '''
		pass

	def get(self, key):
		''' Retrieves a document from the cache (by unique identifier). '''
		pass

	def put(self, key, value, extradata = {}):
		''' Caches a document. '''
		pass

	def delete(self, key):
		''' Remove a document from the cache (by unique identifier). '''
		pass

	def commit(self):
		''' Ensures that all changes are committed to disc. '''
		pass

class NoCache(GenericCache):
	''' Pseudo-class implementing no caching at all. '''

	def __init__(self, *args, **kwargs):
		super(NoCache, self).__init__()
		self.name = 'NoCache'

	def exists(self, key):
		''' Checks if a document is cached. '''
		return False

register(NoCache)

# Setup the NoCache() cache as default...
cache = NoCache()
# Import and register all available caches...
import lltk.caches
