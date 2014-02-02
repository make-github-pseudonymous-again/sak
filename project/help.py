import inspect, project, lib

def list(module = None, action = None):
	if module == None : print(', '.join([o for o, _ in inspect.getmembers(project, inspect.ismodule)]))

	else :
		M = getattr(project, module, None)
		if M == None or not inspect.ismodule(M):
			raise lib.error.ModuleDoesNotExistException(module, project)

		if action == None : print(', '.join([o for o, _ in inspect.getmembers(M, inspect.isfunction)]))

		else :

			A = getattr(M, action, None)
			if A == None or not inspect.isfunction(A):
				raise lib.error.ActionDoesNotExistException(action, M, module)

			print(inspect.formatargspec(*inspect.getargspec(A)))