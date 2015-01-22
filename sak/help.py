import inspect, sak, lib.pacman, lib.check, functools, lib.source , lib.predicate

def ensurefmt ( fmt , n ) :
	fmt = list( fmt )
	if not fmt : fmt = [ print ]
	while len( fmt ) < n : fmt.append( fmt[-1] )
	return tuple( fmt )


def walk ( R , fmt , *path ) :

	fmtR, fmtM, fmtA = ensurefmt(fmt, 3)

	_ , module = lib.sak.resolve( R , path , ['sak'] )

	if module == R : print( fmtR( module ) )

	elif inspect.ismodule( module ) : print( fmtM( module ) )

	else : print( fmtA( module ) )


def info ( *path ) :

	fmtR = functools.partial( lib.pacman.format , pred = inspect.ismodule )
	fmtM = functools.partial( lib.pacman.format , pred = lib.predicate.disjunction( [ inspect.isfunction , inspect.ismodule ] ) )
	fmtA = lambda A : inspect.formatargspec( *inspect.getfullargspec( A ) )

	walk( sak , [ fmtR , fmtM , fmtA ] , *path )


def doc ( *path ) :
	"""
		Print the doc of the specified element (default = sak root module)
	"""

	walk( sak , [ inspect.getdoc ] , *path )


def source ( *path , linenos = False , filename = False ) :
	"""
		Print the source of the specified element (default = sak root module)
	"""

	fmt = functools.partial(lib.source.pretty, linenos = linenos, filename = filename)

	walk( sak , [ fmt ] , *path )
