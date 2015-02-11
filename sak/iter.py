import lib.args, lib.sys, fileinput, itertools, getpass, lib.file

# polyfill for generator zip function

if hasattr( itertools , "izip" ) :
	_zip = itertools.izip

else :
	_zip = zip


def directories ( callable = None , iterable = None ) :

	iterable = lib.args.listify( iterable )
	callable = lib.args.listify( callable )

	callable = list( itertools.chain( *map( lib.args.split , callable ) ) )

	if not iterable :
		iterable = ( s[:-1] for s in fileinput.input( [] ) )

	for item in iterable :

		lib.sys.call( callable , stddefault = None , cwd = item )


def imap ( callable = None , iterable = None ) :

	iterable = lib.args.listify( iterable )
	callable = lib.args.listify( callable )

	callable = list( itertools.chain( *map( lib.args.split , callable ) ) )

	if not iterable :
		iterable = ( s[:-1] for s in fileinput.input( [] ) )

	for item in iterable :

		lib.sys.call( [ arg.format( item ) for arg in callable ] , stddefault = None )


def starmap ( callable = None , iterable = None ) :

	iterable = lib.args.listify( iterable )
	callable = lib.args.listify( callable )

	callable = list( itertools.chain( *map( lib.args.split , callable ) ) )

	if not iterable :
		iterable = ( s[:-1] for s in fileinput.input( [] ) )

	for item in iterable :

		argv = lib.args.split( item )

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


@lib.args.convert( n = int )
def password ( n = -1 ) :

	item = getpass.getpass('Password to repeat : ')
	repeat( item , n )


def izip ( callables = None , sep = " " ) :

	callables = lib.args.listify( callables )

	callables = map( lib.args.split , callables )

	iterables = [ lib.file.lineiterator( lib.sys.popen( callable ).stdout ) for callable in callables ]

	for t in _zip( *iterables ) :

		print ( *t , sep = sep )
