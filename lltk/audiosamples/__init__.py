#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ..helpers import download

def _play_mp3(filename):

	from subprocess import call
	call(['/usr/bin/mpg123', '-q', filename])

from google import google
from forvo import forvo
