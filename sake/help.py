import inspect, sake, lib

def info(module = None, action = None):
	if module is None : print(', '.join([o for o, _ in inspect.getmembers(sake, inspect.ismodule)]))

	else :
		M = getattr(sake, module, None)
		if M is None or not inspect.ismodule(M):
			raise lib.error.ModuleDoesNotExistException(module, sake)

		if action is None : print(', '.join([o for o, _ in inspect.getmembers(M, inspect.isfunction)]))

		else :

			A = getattr(M, action, None)
			if A is None or not inspect.isfunction(A):
				raise lib.error.ActionDoesNotExistException(action, M, module)

			print(inspect.formatargspec(*inspect.getargspec(A)))