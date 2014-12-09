# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import lib.args, lib.sys, fileinput, itertools, getpass


def each ( iterable = None , callable = None ) :

	iterable = lib.args.listify( iterable )
	callable = lib.args.listify( callable )

	if not iterable :
		iterable = ( s[:-1] for s in fileinput.input( [] ) )

	for item in iterable :

		lib.sys.call( [ arg.format( item ) for arg in callable ] , stddefault = None )


def stareach ( iterable = None , callable = None ) :

	iterable = lib.args.listify( iterable )
	callable = lib.args.listify( callable )

	if not iterable :
		iterable = ( s[:-1] for s in fileinput.input( [] ) )

	for item in iterable :

		argv = []

		lib.args.split( item , argv )

		args , kwargs = lib.args.parse( argv , [] , {} )

		lib.sys.call( [ arg.format( *args , **kwargs ) for arg in callable ] , stddefault = None )


@lib.args.convert( n = int )
def repeat ( item , n = -1 ) :

	"""
		Repeat given string n times. If n is negative then repeat given string an infinite number of times.
	"""

	if n < 0 :
		args = [ None ]
	else :
		args = [ None , n ]

	for _ in itertools.repeat( *args ) :
		print( item )


def password ( n = -1 ) :

	item = getpass.getpass('Password to repeat : ')
	repeat( item , n )

