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
			if not self.server:
				self.server = 'localhost'
			if not self.port:
				self.port = 5984
			if not self.database:
				self.database = 'lltk'
			self.couch = couchdb.Server(url = 'http://' + self.server + ':' + str(self.port) + '/')
			from socket import error as SocketError
			try:
				self.db = self.couch[self.database]
			except SocketError:
				# This means that there is no CouchDB instance running...
				from lltk.exceptions import CacheFatalError
				raise CacheFatalError('No CouchDB instance running.')
			except ResourceNotFound:
				# This means that the database does not exist
				if self.setup():
					self.__init__(*args, **kwargs)

		def setup(self):
			''' Runs the initial setup for the CouchDB cache. '''

			self.db = self.couch.create(self.database)
			return True

		def exists(self, key):
			''' Checks if a document is cached. '''

			if key in self.db:
				return True
			return False

		def get(self, key):
			''' Retrieves a document from the CouchDB cache (by unique identifier). '''

			if self.exists(key):
				return self.db[key]['result']
			return None

		def put(self, key, value, extradata = {}):
			''' Caches a document. '''

			document = {'_id' : key, 'result' : value}
			document.update(extradata)

			return self.db.save(document)

		def delete(self, document):
			''' Remove a document from the cache (by unique identifier). '''

			return self.db.delete(document)

		def commit(self):
			''' Ensures that all changes are committed to disc. '''

			return self.db.commit()

	register(CouchDBCache)