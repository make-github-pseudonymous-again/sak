# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import lib.error

try:

	import lxml.etree

	try :
		import urllib.request as urllib2
	except :
		import urllib2

	def href(url, *args):
		conn = urllib2.urlopen(url)
		parser = lxml.etree.HTMLParser(encoding = "utf-8")
		tree = lxml.etree.parse(conn, parser = parser)
		title = tree.find('.//title')
		if title is not None : text = title.text
		else : text = url
		fmt = '<a href="%s">%s</a>'
		print(fmt % (url, text))

		if len(args) : href(*args)

except ImportError as cause:

	e = lib.error.ModuleMissingException(cause, "lxml")

	href = lambda url, *args : lib.error.throw(e)
