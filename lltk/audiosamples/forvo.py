#!/usr/bin/python
# -*- coding: UTF-8 -*-

def forvo(language, word, filename = '', overwrite = False, play = False):
	''' Downloads a suitable audiosample for a given word from Forvo.com. '''

	# @TODO: Normalize volume: mp3gain
	# @TODO: Make forvo() return list of urls, download should not happen here

	import requests

	API_KEY = '4ce2cd9ecb817fa7b27de96b8bb67b10'
	url = 'http://apifree.forvo.com/action/word-pronunciations/format/json/word/%s/language/%s/key/%s/' % (word, language, API_KEY)

	if not len(filename):
		filename = language.upper() + '-' + word + '.mp3'

	page = requests.get(url)
	if page.status_code == 200:
		if 'incorrect' in page.text:
			from ..exceptions import IncorrectForvoAPIKey
			raise IncorrectForvoAPIKey('Your Forvi API key seems to be wrong. Please check on http://api.forvo.com.')
		data = page.json()
		if data == ['Limit/day reached.']:
			from ..exceptions import DailyForvoLimitExceeded
			raise DailyForvoLimitExceeded('You have exceeded your daily Forvo API limit.')
		if data.has_key('items') and len(data['items']):
			# Forvo API can even do the sorting for you. But it's fine for now
			items = sorted(data['items'], key = lambda x: int(x['num_votes']), reverse = True)
			for item in items:
				if item.has_key('pathmp3'):
					mp3url, votes = item['pathmp3'].replace('\\', ''), item['num_votes']
					from . import _download_mp3
					if not _download_mp3(mp3url, filename, overwrite):
						continue
					else:
						if play:
							from . import _play_mp3
							_play_mp3(filename)
						return True
	return False
