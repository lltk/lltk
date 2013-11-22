#!/usr/bin/python
# -*- coding: UTF-8 -*-

def _download_mp3(url, filename, overwrite = False):

	from requests import get
	from os.path import exists

	mp3 = get(url)
	if mp3.status_code == 200:
		if not exists(filename) or overwrite:
			mp3file = open(filename, 'wb')
			mp3file.write(mp3.content)
			mp3file.close()
		return True
	return False

def _play_mp3(filename):

	from subprocess import call
	call(['/usr/bin/mpg123', '-q', filename])

from google import google
