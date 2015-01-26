
import re

_v = 'aeiou'
_V = _v.upper()
_vV = _v + _V

_c = 'zrtypqsdfghjklmwxcvbn'
_C = _c.upper()
_cC = _c + _C


def filt ( s, f ) :
	return ''.join( [c for c in s if c in f] )

vowe  = lambda s: filt( s, _vV )
cons  = lambda s: filt( s, _cC )
vowel = lambda s: filt( s, _v )
consl = lambda s: filt( s, _c )
voweu = lambda s: filt( s, _V )
consu = lambda s: filt( s, _C )


def natural ( s ) :
	return [ int( c ) if c.isdigit() else c for c in re.split( "([0-9]+)", s ) ]

def inside ( a , b ) :
	"""

		Checks if a is inside b, in order.

		>>> from lib.str import *
		>>> inside( "kw" , "keywords" )
		True
		>>> inside( "kywo" , "keywords" )
		True
		>>> inside( "ka" , "keywords" )
		False
		>>> inside( "keeywords" , "keywords" )
		False
		>>> inside( "a" , "action" )
		True
		>>> inside( "a" , "throttled" )
		False

	"""

	i = 0
	j = 0
	m = len( a )
	n = len( b )

	while i < m :

		if n - j < m - i : return False

		if a[i] == b[j] : i += 1

		j += 1

	return True


def utod ( s ) :
	"""
		Replace underscores with dashes.

		>>> from lib.str import *
		>>> utod( "_abc_d_e_" )
		'-abc-d-e-'

	"""
	return s.replace( '_' , '-' )


NAME_RESOLVER = (
	# MATCH
	lambda stringset, alter, string : [ x for x in stringset if alter( x ) == string ] ,
	# PREFIX
	lambda stringset, alter, string : [ x for x in stringset if alter( x ).startswith( string ) ] ,
	# SUFFIX
	lambda stringset, alter, string : [ x for x in stringset if alter( x ).endswith( string ) ] ,
	# SUBSTR
	lambda stringset, alter, string : [ x for x in stringset if string in alter( x ) ]
)

NAME_RESOLVER2 = (
	# INSIDE
	lambda stringset, alter, string : [ x for x in stringset if inside( string , alter( x ) ) ] ,
)


NAME_TRANSFORMER = (
	lambda string : utod( string ) ,
	lambda string : utod( string.lower( ) ) ,
	lambda string : cons( string ) ,
	lambda string : cons( string.lower( ) )
)

NAME_TRANSFORMER2 = (
	NAME_TRANSFORMER[2] , NAME_TRANSFORMER[3] ,
	NAME_TRANSFORMER[0] , NAME_TRANSFORMER[1]
)

NAME_INSPECTORS = (
	(  NAME_TRANSFORMER ,  NAME_RESOLVER ) ,
	( NAME_TRANSFORMER2 , NAME_RESOLVER2 )
)


def mostlikely ( target , stringset ) :

	"""

		Determines which strings out of stringset are most likely to be
		targeted by the target string.

		>>> from lib.str import *
		>>> mostlikely( 'a' , [ 'action' , 'throttled' ] )
		['action']
		>>> mostlikely( '' , [ 'a' , 'b' , 'c' ] )
		[]
		>>> mostlikely( 'kw' , [ 'kwargs' , 'keywords' ] )
		['kwargs']
		>>> mostlikely( 'k' , [ 'kwargs' , 'keywords' ] )
		['kwargs', 'keywords']
		>>> mostlikely( 'kw' , [ 'username' , 'keywords' ] )
		['keywords']
		>>> mostlikely( 'x-y' , [ 'X_Y' , 'x_y' , 'XY' , 'xy' ] )
		['x_y']
		>>> mostlikely( 'X-Y' , [ 'X_Y' , 'x_y' , 'XY' , 'xy' ] )
		['X_Y']
		>>> mostlikely( 'xy' , [ 'X_Y' , 'x_y' , 'XY' , 'xy' ] )
		['xy']
		>>> mostlikely( 'XY' , [ 'X_Y' , 'x_y' , 'XY' , 'xy' ] )
		['XY']
		>>> mostlikely( 'x-y' , [ 'XY' , 'xy' ] )
		['xy']
		>>> mostlikely( 'X-Y' , [ 'XY' , 'xy' ] )
		['XY']
		>>> mostlikely( 'xy' , [ 'X_Y' , 'x_y' ] )
		['x_y']
		>>> mostlikely( 'XY' , [ 'X_Y' , 'x_y' ] )
		['X_Y']

	"""

	for transformers , resolvers in NAME_INSPECTORS :

		for alter in transformers :

			string = alter( target )

			# if alter reduces target to the empty
			# string do not forget to skip
			if not string : continue

			for resolver in resolvers :
				matching = resolver( stringset, alter, string )

				if len( matching ) > 0 :
					return matching

	return []
