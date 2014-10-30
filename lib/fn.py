# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals



def callable(fn):
	return hasattr(fn, '__call__')


def val(o, *args, **kwargs):
	if callable(o) : return o(*args, **kwargs)
	else           : return o
