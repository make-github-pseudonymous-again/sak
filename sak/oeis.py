import urllib.request

TEXT = "http://oeis.org/search?q=id:%s&fmt=text"
OEIS = "https://oeis.org/%s"

MONTHS = [ "Jan" , "Feb" , "Mar" , "Apr" , "May" , "Jun" , "Jul" , "Aug" , "Sep" , "Oct" , "Nov" , "Dec" ]

def validate ( id ) :

	if len( id ) != 7 :

		print( "ERROR-1: Bad length!" )
		return False

	first , *sequence = id

	if first != "A" :

		print( "ERROR-3: The Sequence does not begin with A." )
		return False

	digits = set( "0123456789" )

	for d in sequence :

		if d not in digits :

			print("ERROR-2: Wrong characters on input string!")
			return False

	return True


def bibtex ( id ) :

	r"""

		>>> from sak.oeis import bibtex
		>>> bibtex( "A00004" )
		ERROR-1: Bad length!
		>>> bibtex( "B000045" )
		ERROR-3: The Sequence does not begin with A.
		>>> bibtex( "A0P0045" )
		ERROR-2: Wrong characters on input string!
		>>> bibtex( "A000045" ) # doctest: +NORMALIZE_WHITESPACE
		@MISC{OEIS:A000045,
			AUTHOR       = {N. J. A. Sloane},
			TITLE        = {The {O}n-{L}ine {E}ncyclopedia of {I}nteger {S}equences},
			HOWPUBLISHED = {\href{https://oeis.org/A000045}{A000045}},
			MONTH        = {Apr},
			YEAR         = {1991},
			NOTE         = {Fibonacci numbers: F(n) = F(n-1) + F(n-2) with F(0) = 0 and F(1) = 1.}
		}
		>>> bibtex( "A000108" ) # doctest: +NORMALIZE_WHITESPACE
		@MISC{OEIS:A000108,
			AUTHOR       = {N. J. A. Sloane},
			TITLE        = {The {O}n-{L}ine {E}ncyclopedia of {I}nteger {S}equences},
			HOWPUBLISHED = {\href{https://oeis.org/A000108}{A000108}},
			MONTH        = {},
			YEAR         = {},
			NOTE         = {Catalan numbers: C(n) = binomial(2n,n)/(n+1) = (2n)!/(n!(n+1)!). Also called Segner numbers.}
		}

	"""

	if not validate( id ) : return

	url = TEXT % id

	try :

		response = urllib.request.urlopen( url )

	except urllib.error.HTTPError as e :

		print( e , ": could not open url %s" % url )
		return

	data = response.read( )
	lines = data.decode( "utf-8" ).splitlines( )

	month , day , year = "" , "" , ""

	for line in lines :

		if line.startswith( "%A" ) :

			author = line[11:]

			for m in MONTHS :

				x = author.rfind( m )

				if x >= 0 :

					month , day , year = author[x:].split( )
					author = author[:x]
					break

			author = ", ".join( x.strip( " _" ) for x in author.strip( ).split("," ) if x )

		if line.startswith( "%N" ) : description = line[11:]

	print( r"""@MISC{OEIS:%s,
	AUTHOR       = {%s},
	TITLE        = {The {O}n-{L}ine {E}ncyclopedia of {I}nteger {S}equences},
	HOWPUBLISHED = {\href{%s}{%s}},
	MONTH        = {%s},
	YEAR         = {%s},
	NOTE         = {%s}
}""" % ( id , author , OEIS % id , id , month , year , description ) )
