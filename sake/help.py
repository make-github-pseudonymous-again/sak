import inspect, sake, lib

def info(module = None, action = None):
	if module == None : print(', '.join([o for o, _ in inspect.getmembers(sake, inspect.ismodule)]))

	else :
		M = getattr(sake, module, None)
		if M == None or not inspect.ismodule(M):
			raise lib.error.ModuleDoesNotExistException(module, sake)

		if action == None : print(', '.join([o for o, _ in inspect.getmembers(M, inspect.isfunction)]))

		else :

			A = getattr(M, action, None)
			if A == None or not inspect.isfunction(A):
				raise lib.error.ActionDoesNotExistException(action, M, module)

			print(inspect.formatargspec(*inspect.getargspec(A)))