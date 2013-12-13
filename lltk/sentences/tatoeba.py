#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import html

def tatoeba(language, word):
	mapto = {'it' : 'ita', 'en' : 'eng', 'de': 'deu', 'es' : 'spa', 'nl' : 'nld', 'fr' : 'fra'}
	if not mapto.has_key(language):
		raise LanguageNotSupported('The language ' + language.upper() + ' is not supported so far.')

	word, sentences = unicode(word), []
	page = requests.get('http://tatoeba.org/deu/sentences/search?query=%s&from=%s&to=und' % (word, mapto[language]))
	tree = html.fromstring(page.text)
	for sentence in tree.xpath('//div[@class="sentence mainSentence"]/div/a/text()'):
		sentence = sentence.encode('iso-8859-1').decode('utf-8')
		if word in sentence and len(sentence) < 100 and len(sentence) > 15:
			sentences.append(sentence)
	return sentences
