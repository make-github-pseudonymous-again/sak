
import os.path , lib.check , lib.pacman

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
