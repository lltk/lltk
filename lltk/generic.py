#!/usr/bin/python
# -*- coding: UTF-8 -*-

__all__ = ['articles', 'plural', 'ipa', 'miniaturize', 'reference', 'translate', 'audiosample', 'samplesentence']

from decorators import _load_language, _load_language_or_die

@_load_language_or_die
def pos(language, word):
	''' Returns a list of possible POS-tags (part-of-speech) for a given word. '''
	pass

@_load_language_or_die
def articles(language, word):
	''' Returns the articles (singular and plural) for a given noun. '''
	pass

@_load_language_or_die
def plural(language, word):
	''' Returns the plural form for a given noun. '''
	pass

@_load_language_or_die
def conjugate(language, word):
	''' Returns the conjugation of a given verb. '''
	pass

@_load_language_or_die
def ipa(language, word):
	''' Returns the International Phonetic Alphabet (IPA) writing for a given word. '''
	pass

@_load_language_or_die
def gender(language, word):
	''' Returns the gender for a given noun. '''
	pass

@_load_language_or_die
def miniaturize(language, word):
	''' Returns the miniaturized version for a given noun. '''
	pass

@_load_language
def reference(language, word):
	''' Returns the articles (singular and plural) combined with singular and plural for a given noun. '''
	return ['%s %s' % (article(language, word)[0] or '-', word), '%s %s' % (article(language, word)[1] or '-', plural(language, word)[0] or '-')]

@_load_language
def translate(language, word):
	''' Translates a word using Google Translate. '''

	from textblob import TextBlob
	return TextBlob(word).translate(from_lang = language[0], to = language[1]).string

@_load_language
def audiosample(language, word, filename = '', play = False):
	''' Returns a suitable audiosample for a given word '''

	from lltk.audiosamples import forvo, google
	if forvo(language, word, filename, play = play):
		return True
	return google(language, word, filename, play = play)

@_load_language
def samplesentence(language, word):
	''' Returns a sample sentence showing a given word in context.'''

	from lltk.sentences import tatoeba
	return tatoeba(language, word)
