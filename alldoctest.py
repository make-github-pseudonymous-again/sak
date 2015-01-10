#!/usr/bin/env python3

import os, sys, doctest

def doctestrecurse ( source ) :

	if os.path.isfile( source ) :

		if source[-3:] == ".py" :

			print( source )

			return doctest.testfile( source )

	elif os.path.isdir( source ) :

		failurecount, testcount = 0, 0

		for child in os.listdir( source ) :

			fc, tc = doctestrecurse( os.path.join( source, child ) )

			failurecount += fc
			testcount += tc

		return failurecount, testcount

	return 0, 0


failurecount, testcount = doctestrecurse( "lib" )

sys.exit( failurecount )
