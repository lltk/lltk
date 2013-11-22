#!/usr/bin/python
# -*- coding: UTF-8 -*-

from decorators import load_language, load_language_or_die

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
def samplesentence(language, word):

	mapto = {'it' : 'ita', 'en' : 'eng', 'de': 'deu', 'es' : 'spa', 'nl' : 'nld', 'fr' : 'fra'}
	if not mapto.has_key(language):
		raise LanguageNotSupported('The language ' + language.upper() + ' is not supported so far.')

	from requests import get
	from lxml import html

	word, sentences = unicode(word), []
	page = get('http://tatoeba.org/deu/sentences/search?query=%s&from=%s&to=und' % (word, mapto[language]))
	tree = html.fromstring(page.text)
	for sentence in tree.xpath('//div[@class="sentence mainSentence"]/div/a/text()'):
		sentence = sentence.encode('iso-8859-1').decode('utf-8')
		if word in sentence and len(sentence) < 100 and len(sentence) > 15:
			sentences.append(sentence)
	return sentences
