import inspect, sake, lib

def info(module = None, action = None):
	if module is None :
		print(lib.pacman.format(sake, inspect.ismodule))

	else :
		M = getattr(sake, module, None)
		lib.check.ModuleDoesNotExistException(M, module, sake)

		if action is None :
			print(lib.pacman.format(M, inspect.isfunction))

		else :

			A = getattr(M, action, None)
			lib.check.ActionDoesNotExistException(A, action, M, module)

			print(inspect.formatargspec(*inspect.getargspec(A)))