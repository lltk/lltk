#!/usr/bin/python
# -*- coding: UTF-8 -*-

__all__ = ['CouchDBCache']

try:
	from couchcache import CouchDBCache
	del couchcache
except ImportError:
	pass