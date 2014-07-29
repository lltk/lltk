#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import html
import lltk.locale

def tatoeba(language, word, minlength = 10, maxlength = 100):
	''' Returns a list of suitable textsamples for a given word using Tatoeba.org. '''

	word, sentences = unicode(word), []
	page = requests.get('http://tatoeba.org/deu/sentences/search?query=%s&from=%s&to=und' % (word, lltk.locale.iso639_1to3(language)))
	tree = html.fromstring(page.text)
	for sentence in tree.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " mainSentence ")]/div/a/text()'):
		sentence = sentence.strip(u' "„“').replace(u'“ „', u' – ').replace('" "', u' – ')
		if word in sentence and len(sentence) < maxlength and len(sentence) > minlength:
			sentences.append(sentence)
	return sentences
