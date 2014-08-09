#!/usr/bin/python
# -*- coding: UTF-8 -*-

__all__ = ['pos', 'articles', 'plural', 'conjugate', 'ipa', 'gender', 'miniaturize', 'comparative', 'superlative', 'reference', 'translate', 'audiosamples', 'textsamples', 'images']

from lltk.decorators import _load_language, _load_language_or_die

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
def conjugate(language, word, tense):
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

@_load_language_or_die
def comparative(language, word):
	''' Returns the comparative for a given adjective. '''
	pass

@_load_language_or_die
def superlative(language, word):
	''' Returns the superlative for a given adjective. '''
	pass

@_load_language
def reference(language, word):
	''' Returns the articles (singular and plural) combined with singular and plural for a given noun. '''

	sg, pl, art = word, '/'.join(plural(language, word)  or ['-']), [[''], ['']]
	art[0], art[1] = articles(language, word) or (['-'], ['-'])
	result = ['%s %s' % ('/'.join(art[0]), sg), '%s %s' % ('/'.join(art[1]), pl)]
	result = [None if x == '- -' else x for x in result]
	return result

@_load_language
def translate(language, word):
	''' Translates a word using Google Translate. '''

	from textblob import TextBlob
	return TextBlob(word).translate(from_lang = language[0], to = language[1]).string

@_load_language
def audiosamples(language, word, key = ''):
	''' Returns a list of URLs to suitable audiosamples for a given word. '''

	from lltk.audiosamples import forvo, google

	urls = []
	urls += forvo(language, word, key)
	urls += google(language, word)
	return urls

@_load_language
def textsamples(language, word):
	''' Returns a sample sentence showing a given word in context.'''

	from lltk.textsamples import tatoeba
	return tatoeba(language, word)

@_load_language
def images(language, word, n = 20, *args, **kwargs):
	''' Returns a list of URLs to suitable images for a given word.'''

	from lltk.images import google
	return google(language, word, n, *args, **kwargs)
