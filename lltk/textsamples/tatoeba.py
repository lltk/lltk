#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from lxml import html
import lltk.locale

def tatoeba(language, word):

	word, sentences = unicode(word), []
	page = requests.get('http://tatoeba.org/deu/sentences/search?query=%s&from=%s&to=und' % (word, lltk.locale.iso639_1to3(language)))
	tree = html.fromstring(page.text)
	for sentence in tree.xpath('//div[@class="sentence mainSentence"]/div/a/text()'):
		sentence = sentence.encode('iso-8859-1').decode('utf-8')
		if word in sentence and len(sentence) < 100 and len(sentence) > 15:
			sentences.append(sentence)
	return sentences
