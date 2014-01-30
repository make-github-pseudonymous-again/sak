#!/usr/bin/python3

import sys, project, inspect


def main(arg):

	if len(arg) < 1 : raise project.error.ModuleNameNotSpecifiedException(project)
	module = getattr(project, arg[0], None)
	if module == None or not inspect.ismodule(module): raise project.error.ModuleDoesNotExistException(arg[0], project)

	if len(arg) < 2 : raise project.error.ActionNameNotSpecifiedException(module, arg[0])
	action = getattr(module, arg[1], None)
	if action == None or not inspect.isfunction(action): raise project.error.ActionDoesNotExistException(arg[1], module, arg[0])

	spec = inspect.getargspec(action)
	m = (0 if spec[0] == None else len(spec[0])) - (0 if spec[3] == None else len(spec[3]))
	n = len(arg) - 2
	if n < m : raise project.error.TooFewArgumentsForActionException(n, spec, arg[1], arg[0])
	if spec[1] == None and n > len(spec[0]) : raise project.error.TooManyArgumentsForActionException(n, spec, arg[1], arg[0])
	action(*arg[2:])


if __name__ == '__main__':

	try : main(sys.argv[1:])
	except project.error.MainException as e : print(e)
