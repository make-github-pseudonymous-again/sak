from __future__ import absolute_import, division, print_function, unicode_literals

import lib.sys

def stdin():
	lib.sys.call(["xclip", "-i", "-selection", "c"], stddefault = None)

def stdout():
	lib.sys.call(["xclip", "-o", "-selection", "c"], stddefault = None)