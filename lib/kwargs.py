from __future__ import absolute_import, division, print_function, unicode_literals

import inspect

def filter(kwargs, fn):
	args = inspect.getargspec(fn).args
	return { key : kwargs[key] for key in args if key in kwargs}