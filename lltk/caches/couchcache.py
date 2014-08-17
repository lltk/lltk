#!/usr/bin/python
# -*- coding: UTF-8 -*-

try:
	import couchdb
	from couchdb import ResourceNotFound
except ImportError:
	couchdb = None

if couchdb:

	from lltk.caching import GenericCache, register

	class CouchDBCache(GenericCache):
		''' Uses CouchDB as cache backend. '''

		def __init__(self, *args, **kwargs):

			super(CouchDBCache, self).__init__(*args, **kwargs)
			self.name = 'CouchDB'
			self.couch = None
			self.db = None
			if not self.server:
				self.server = 'localhost'
			if not self.port:
				self.port = 5984
			if not self.database:
				self.database = 'lltk'

		def connect(self):
			''' Establishes the connection to the backend. '''

			from socket import error as SocketError
			self.couch = couchdb.Server(url = 'http://' + self.server + ':' + str(self.port) + '/')
			try:
				self.db = self.couch[self.database]
			except SocketError:
				# This means that there is no CouchDB instance running...
				from lltk.exceptions import CacheFatalError
				raise CacheFatalError('No CouchDB instance running.')
			except ResourceNotFound:
				# This means that the database does not exist
				if self.setup():
					self.connect()
			self.connection = True

		def setup(self):
			''' Runs the initial setup for the CouchDB cache. '''

			self.db = self.couch.create(self.database)
			return True

		@GenericCache.needsconnection
		def exists(self, key):
			''' Checks if a document is cached. '''

			if key in self.db:
				return True
			return False

		@GenericCache.needsconnection
		def get(self, key):
			''' Retrieves a document from the CouchDB cache (by unique identifier). '''

			if self.exists(key):
				return self.db[key]['result']
			return None

		@GenericCache.needsconnection
		def put(self, key, value, extradata = {}):
			''' Caches a document. '''

			document = {'_id' : key, 'result' : value}
			document.update(extradata)

			return self.db.save(document)

		@GenericCache.needsconnection
		def delete(self, document):
			''' Remove a document from the cache (by unique identifier). '''

			return self.db.delete(document)

		@GenericCache.needsconnection
		def commit(self):
			''' Ensures that all changes are committed to disc. '''

			return self.db.commit()

	register(CouchDBCache)