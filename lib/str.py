
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



NAME_RESOLVER = [
	# MATCH
	lambda stringset, alter, string : [x for x in stringset if alter(x) == string],
	# PREFIX
	lambda stringset, alter, string : [x for x in stringset if alter(x).startswith(string)],
	# SUFFIX
	lambda stringset, alter, string : [x for x in stringset if alter(x).endswith(string)],
	# SUBSTR
	lambda stringset, alter, string : [x for x in stringset if string in alter(x)]
]


NAME_TRANSFORMER = [
	lambda string : string,
	lambda string : string.lower(),
	lambda string : cons( string ),
	lambda string : cons( string.lower() )
]


def mostlikely ( target, stringset ) :

	for alter in NAME_TRANSFORMER:
		string = alter( target )

		for resolver in NAME_RESOLVER:
			matching = resolver( stringset, alter, string )

			if len( matching ) > 0 :
				return matching

	return []
