from __future__ import absolute_import, division, print_function, unicode_literals

import lib.sys

NAVIGATOR = "google-chrome"

def open(url):
	lib.sys.call([NAVIGATOR, url]);