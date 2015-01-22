
import os.path , inspect , lib.check , lib.pacman , lib.args , lib.fn , lib.str

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
BIN = os.path.join(ROOT, "bin")
LIB = os.path.join(ROOT, "lib")
SAK = os.path.join(ROOT, "sak")
DATA = os.path.join(ROOT, "data")

def data(*path):
	return os.path.join(DATA, *path)

def findaction ( module , inp , hierarchy ) :

	# DETERMINE MODULE

	i = 0

	while True :

		parent = '.'.join(hierarchy)

		lib.check.ModuleOrActionNameSpecified( parent , module , inp , i )
		moduleName = inp[i]

		modules = lib.pacman.resolve( moduleName , module )

		lib.check.ModuleOrActionNameExists( parent, module , moduleName , modules )
		lib.check.ModuleOrActionNameNotAmbiguous( parent, moduleName, modules )

		moduleName = modules[0]
		module = getattr( module , moduleName )

		hierarchy.append( moduleName )

		i += 1

		if lib.fn.callable( module ) : break

	return hierarchy , module , inp[i:]


def resolve ( module , inp , hierarchy ) :

	# DETERMINE MODULE

	for part in inp :

		parent = '.'.join(hierarchy)

		modules = lib.pacman.resolve( part , module )

		lib.check.ModuleOrActionNameExists( parent, module , part , modules )
		lib.check.ModuleOrActionNameNotAmbiguous( parent, part, modules )

		part = modules[0]
		module = getattr( module , part )

		hierarchy.append( part )

	return hierarchy , module


def assignarguments ( hierarchy, action, inp ) :

	# CHECK ACTION ARGUMENTS

	moduleName = ".".join( hierarchy[:-1] )
	actionName = hierarchy[-1]

	args, kwargs = lib.args.parse( inp, [], {} )

	spec = inspect.getfullargspec( action )

	kwargslist = lib.args.kwargslist( spec )

	if kwargs :

		lib.check.KwargsNotSupportedException( actionName, kwargslist )

		_kwargs = dict()

		for kwarg in kwargs :

			matching = lib.str.mostlikely( kwarg, kwargslist )

			if not matching and spec.varkw :
				_kwargs[kwarg] = kwargs[kwarg]
			else :
				lib.check.KwargNameExists( kwarg, actionName, matching, kwargslist )
				lib.check.KwargNameNotAmbiguous( kwarg, actionName, matching )

				_kwargs[matching[0]] = kwargs[kwarg]

		kwargs = _kwargs

	# WE INFLATE AFTER RESOLVING KWARGS THUS
	# KWARGS IN JSON ARGS FILES MUST BE
	# EXACTLY MATCHING SPECS OF ACTIONS

	lib.args.inflate( args, kwargs )

	m = ( 0 if spec[0] is None else len( spec[0] ) ) -\
	    ( 0 if spec[3] is None else len( spec[3] ) )
	n = len( args )

	lib.check.NotTooFewArgumentsForAction( moduleName, actionName, n, m, spec )
	lib.check.NotTooManyArgumentsForAction( moduleName, actionName, n, m, spec )


	# DONE
	return args, kwargs


