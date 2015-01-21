import inspect, sak, lib.pacman, lib.check, functools, lib.source

def ensurefmt(fmt, n):
	fmt = list(fmt)
	if not fmt : fmt = [print,]
	while len(fmt) < n : fmt.append(fmt[-1])
	return tuple(fmt)


def walk(R, module, action, *fmt):


	fmtR, fmtM, fmtA = ensurefmt(fmt, 3)

	if module is None :
		print(fmtR(R))

	else :

		parent = "sak"

		M = lib.pacman.resolve( module , R )

		lib.check.ModuleOrActionNameExists( parent , R , module , M )
		lib.check.ModuleOrActionNameNotAmbiguous( parent , module , M )

		module = M[0]

		M = getattr( R , module )

		if action is None :
			print(fmtM(M))

		else :

			parent += "." + module

			A = lib.pacman.resolve( action , M )

			lib.check.ModuleOrActionNameExists( parent , M , action , A )
			lib.check.ModuleOrActionNameNotAmbiguous( parent , action , A )

			action = A[0]

			A = getattr( M , action )

			print(fmtA(A))


def info(module = None, action = None):

	fmtR = functools.partial(lib.pacman.format, pred = inspect.ismodule)
	fmtM = functools.partial(lib.pacman.format, pred = inspect.isfunction)
	fmtA = lambda A : inspect.formatargspec(*inspect.getfullargspec(A))

	walk(sak, module, action, fmtR, fmtM, fmtA)


def doc(module = None, action = None):
	"""
		Print the doc of the specified element (default = sak root module)
	"""

	walk(sak, module, action, inspect.getdoc)


def source(module = None, action = None, linenos = False, filename = False):
	"""
		Print the source of the specified element (default = sak root module)
	"""

	fmt = functools.partial(lib.source.pretty, linenos = linenos, filename = filename)

	walk(sak, module, action, fmt)
