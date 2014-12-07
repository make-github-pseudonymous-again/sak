# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import lib.args, lib.sys, fileinput

def each ( iterable = None , callable = None ) :

	iterable = lib.args.listify( iterable )
	callable = lib.args.listify( callable )

	if not iterable :
		iterable = ( s[:-1] for s in fileinput.input( [] ) )

	for item in iterable :

		lib.sys.call( [ arg.replace( "%i", item ) for arg in callable ] , stddefault = None )


@lib.args.convert( n = int )
def repeat ( item , n ) :

	for i in range( n ) :
		print( item )



