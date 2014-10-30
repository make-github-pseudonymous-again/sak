# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals



def sentinel(n, a, b = None):
	for i in range(n - 1) : yield a
	yield b
