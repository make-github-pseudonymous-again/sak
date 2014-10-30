# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


OUT = ['aux', 'idx', 'log', 'out', 'pyg', 'pdf', 'toc']

def out(name):
	for ext in OUT:
		yield '%s.%s' % (name, ext)
