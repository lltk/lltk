Language Learning Toolkit
=======

The Language Learning Toolkit combines several approaches such as natural language processing and web scraping to perform a variety of tasks useful for (human) language learning.
This includes:

 * Part-of-speech tagging (POS) supported by [Pattern](http://github.com/clips/pattern)
 * Phonetic transcriptions in accordance with the [International Phonetic Alphabet](http://en.wikipedia.org/wiki/International_Phonetic_Alphabet) (IPA)
 * Audiosamples ([Forvo](http://www.forvo.com/), Google Translate)
 * Textsamples/Sample sentences ([Tatoeba](http://tatoeba.org/))
 * Visual representations of a given word using Google Images
 * Conjugation of verbs (Present, Perfect, Past, Pluperfect, Future) supported by [Verbix](www.verbix.com/)
 * Pluralization of nouns (accuracy depending on the language)
 * Indefinite and definite articles for nouns (accuracy depending on the language)
 * Comparative and superlative for adjectives
 * Basic gender detection for nouns

General information
-------------------

Everything inside LLTK is split up into different modules, allowing for a maximum of flexibility and interchangeability. In fact, each language is a module for itself. When calling a language-specific function, you can choose between addressing the module directly (e.g. `lltk.nl.plural('hond')`), or using the generic interface (e.g. `lltk.generic.plural('nl', 'hond')`). Both calls will pass down the request to an appropriate scraper and can be considered equivalent.

To get a quick overview of LLTK's syntax, launch [IPython](http://ipython.org/), `import lltk` and start browsing using tab completion. If you want, you can enable the debug mode by setting `lltk.config['debug'] = True`.

Examples
--------

The syntax should be pretty straightforward and intuitive. Nevertheless, you might want to have a look at the following examples:

 * **IPA**: `lltk.generic.ipa('de', 'Blume')` returns a list of possible IPA writings or `None`.
 * **Pluralization**: `lltk.generic.plural('nl', 'boom')` returns a list of plural forms or `None`.

 Some scrapers know when there's no plural form of a given word. They will return `['']`.
 * **Definite/Indefinite articles**: `lltk.generic.articles('de', 'Katze')` returns a list of lists of valid articles (singular and plural). Have a look at `lltk.generic.reference` as well.

When using the generic interface, LLTK will raise the `NotImplementedError` exception if the desired functionality is not available in your target language.

 * For **conjugation of verbs**, try the following:
 ```python
 lltk.generic.conjugate('de', 'bauen', 'present')
 lltk.generic.conjugate('de', 'bauen', 'past')
 lltk.generic.conjugate('de', 'bauen', 'perfect')
 ```

 * If you want to listen to **audio samples**, register at Forvo and get your [API key](http://api.forvo.com/). Then paste:
 ```python
 urls = lltk.generic.audiosamples('it', 'mela', key = '---')
 lltk.helpers.download(urls[0], '/tmp/audiosample-it-mela.mp3')
 lltk.helpers.play('/tmp/audiosample-it-mela.mp3')
 ```

 * To see a word used in context, request **sample sentences** (currently using [Tatoeba](http://tatoeba.org/)). Try:
 ```python
 sentences = lltk.generic.textsamples('es', u'jardín')
 for sentence in sentences:
 	print sentence
 ```

 * **View images** related to a given word (currently using [Google Images](http://images.google.com/)). Try the following:
 ```python
 photos = lltk.generic.images('fr', u'souris')
 clipart = lltk.generic.images('fr', u'souris', itype = 'clipart', isize = 'large')
 lineart = lltk.generic.images('fr', u'souris', itype = 'lineart', isize = 'small')
 ```

Requirements
------------

The Language Learning Toolkit is written for Python 2.7. There is no support for Python 3, yet. Please install the following Python packages: [requests](https://pypi.python.org/pypi/requests/), [lxml](https://pypi.python.org/pypi/lxml/3.3.5), [Pattern](https://pypi.python.org/pypi/Pattern/2.6), [functools32](https://pypi.python.org/pypi/functools32/3.2.3-1). You can do that by running:

`sudo pip install -r requirements/base.txt`

Furthermore, we highly encourage you to install `CouchDB` for caching. If you are a developer, you should probably install everything from `base.txt`, `extra.txt` and `development.txt`.

License
-------

**GNU Lesser General Public License (LGPL)**, see `LICENSE.txt` for further details.
