#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import json

from lltk.helpers import debug

def google(language, word, n = 20, *args, **kwargs):
	''' Downloads suitable images for a given word from Google Images. '''

	if not kwargs.has_key('start'):
		kwargs['start'] = 0
	if not kwargs.has_key('itype'):
		kwargs['itype'] = 'photo|clipart|lineart'
	if not kwargs.has_key('isize'):
		kwargs['isize'] = 'small|medium|large|xlarge'
	if not kwargs.has_key('filetype'):
		kwargs['filetype'] = 'jpg'

	info = {'q' : word, 'hl' : language, 'start' : str(kwargs['start']), 'as_filetype' : kwargs['filetype'], 'imgsz' : kwargs['isize'], 'imgtype' : kwargs['itype'], 'rsz' : '8', 'safe' : 'active'}
	query = '&'.join([x[0] + '=' + x[1] for x in info.items()])
	url = 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&' + query

	debug('Loading ' + unicode(url) + '...')
	page = requests.get(url)
	data = json.loads(page.text)
	images = []

	if data and data.has_key('responseData') and data['responseData']:
		items = data['responseData']['results']
		if items:
			images += [item['url'] for item in items]
			if len(images) < n:
				kwargs['start'] += 8
				images += google(language, word, n, *args, **kwargs)
	return images[:n]
