from __future__ import absolute_import, division, print_function, unicode_literals

import lib.sys

def cut(source, dest, start, end):
	lib.sys.call([
		"pdftk",
		"A=%s" % source,
		"cat",
		"A%d-%d" % (start, end),
		"output",
		dest
	], stddefault = None)


def burst(source):
	lib.sys.call([
		"pdftk",
		source,
		"burst"
	], stddefault = None)

def svg(source):
	lib.sys.call([
		"pdftocairo",
		"-svg",
		source
	], stddefault = None)