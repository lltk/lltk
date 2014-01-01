#!/usr/bin/python
# -*- coding: UTF-8 -*-

def google(language, word, filename = '', overwrite = False, play = False):
	''' Downloads a suitable audiosample for a given word from Google Translate. '''

	from . import download

	mp3url = 'http://translate.google.com/translate_tts?tl=%s&q=%s' % (language, word)

	if not len(filename):
		filename = language.upper() + '-' + word + '.mp3'
	if download(mp3url, filename, overwrite):
		if play:
			from . import _play_mp3
			_play_mp3(filename)
		return True
	return False
