#!/usr/bin/python
# -*- coding: UTF-8 -*-

def google(language, word):
	''' Returns a list of suitable audiosamples for a given word from Google Translate. '''

	url = 'http://translate.google.com/translate_tts?tl=%s&q=%s' % (language, word)
	return [url]
