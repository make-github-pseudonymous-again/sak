# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import lib.inspect

def filter ( kwargs, fn ) :
	args = lib.inspect.getargspec(fn).args
	return dict( (key, kwargs[key]) for key in args if key in kwargs )
