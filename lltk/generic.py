#!/usr/bin/python
# -*- coding: UTF-8 -*-

from decorators import load_language, load_language_or_die

LANGUAGES = ['de', 'en', 'nl', 'it', 'fr']

@load_language_or_die
def article(language, word):
	''' Returns the correct articles (singular and plural) for a given word. '''
	pass

@load_language_or_die
def plural(language, word):
	''' Returns the plural version for a given word. '''
	pass

@load_language_or_die
def gender(language, word):
	''' Returns the gender for a given word. '''
	pass

@load_language_or_die
def miniaturize(language, word):
	''' Returns the gender for a given word. '''
	pass

@load_language_or_die
def ipa(language, word):
	''' Returns the IPA writing for a given word. '''
	pass

@load_language
def reference(language, word):
	''' Example: reference('tree') -> ['the tree', 'the trees']. '''
	return ['%s %s' % (article(language, word)[0] or '-', word), '%s %s' % (article(language, word)[1] or '-', plural(language, word)[0] or '-')]

@load_language
def translate(language, word):
	''' Translates a word using Google Translate. '''

	from textblob import TextBlob
	return TextBlob(word).translate(from_lang = language[0], to = language[1]).string

@load_language
def audiosample(language, word, filename = '', play = False):
	''' Tries to find a suitable audiosample for a given word '''

	import lltk.audiosamples
	if lltk.audiosamples.forvo(language, word, filename, play = play):
		return True
	return lltk.audiosamples.google(language, word, filename, play = play)

@load_language
def samplesentence(language, word):

	from lltk.sentences import tatoeba
	return tatoeba(language, word)
