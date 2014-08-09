#!/usr/bin/python
# -*- coding: UTF-8 -*-

def forvo(language, word, key):
	''' Returns a list of suitable audiosamples for a given word from Forvo.com. '''

	from requests import get

	url = 'http://apifree.forvo.com/action/word-pronunciations/format/json/word/%s/language/%s/key/%s/' % (word, language, key)
	urls = []

	page = get(url)
	if page.status_code == 200:
		if 'incorrect' in page.text:
			from lltk.exceptions import IncorrectForvoAPIKey
			raise IncorrectForvoAPIKey('Your Forvi API key seems to be wrong. Please check on http://api.forvo.com.')
		data = page.json()
		if data == ['Limit/day reached.']:
			from lltk.exceptions import DailyForvoLimitExceeded
			raise DailyForvoLimitExceeded('You have exceeded your daily Forvo API limit.')
		if data.has_key('items') and len(data['items']):
			items = sorted(data['items'], key = lambda x: int(x['num_votes']), reverse = True)
			for item in items:
				urls.append(item['pathmp3'])
	return urls
