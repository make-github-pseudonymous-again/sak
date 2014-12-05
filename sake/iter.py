# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import lib.args, lib.sys

def each ( iterable = None , callable = None ) :

	iterable = lib.args.listify( iterable )
	callable = lib.args.listify( callable )

	for item in iterable :

		lib.sys.call( [ item if arg == "%i" else arg for arg in callable ] , stddefault = None )
 
