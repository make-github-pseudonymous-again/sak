#!/usr/bin/python3
from __future__ import absolute_import, division, print_function, unicode_literals

import os, doctest

def recurse ( source ) :

	if os.path.isfile( source ) :

		if source[-3:] == ".py" :

			print( source )

			doctest.testfile( source )

	elif os.path.isdir( source ) :

		for child in os.listdir( source ) :

			recurse( os.path.join( source, child ) )

recurse( "lib" )
