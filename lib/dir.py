from __future__ import absolute_import, division, print_function, unicode_literals

import os, functools

def walk(s, d = None, f = print):
	if d is None : d = functools.partial(walk, d = d, f = f) 
	for e in sorted(os.listdir(s)):
		path = os.path.join(s, e)

		if   d and os.path.isdir(path)  : d(path)
		elif f and os.path.isfile(path) : f(path)