#!/usr/bin/python3

import sys, project, inspect, lib


def main(inp):

	action, arguments = parse(inp)
	action(*arguments)


def parse(inp):
	# Determine module
	if len(inp) < 1:
		raise lib.error.ModuleNameNotSpecifiedException(project)

	module = getattr(project, inp[0], None)
	if module == None or not inspect.ismodule(module):
		raise lib.error.ModuleDoesNotExistException(inp[0], project)

	# Determine action
	if len(inp) < 2:
		raise lib.error.ActionNameNotSpecifiedException(module, inp[0])

	action = getattr(module, inp[1], None)
	if action == None or not inspect.isfunction(action):
		raise lib.error.ActionDoesNotExistException(inp[1], module, inp[0])

	# Check action arguments
	spec = inspect.getargspec(action)
	m = (0 if spec[0] == None else len(spec[0])) - (0 if spec[3] == None else len(spec[3]))
	n = len(inp) - 2

	if n < m:
		raise lib.error.TooFewArgumentsForActionException(n, spec, inp[1], inp[0])

	if spec[1] == None and n > len(spec[0]):
		raise lib.error.TooManyArgumentsForActionException(n, spec, inp[1], inp[0])

	# Done
	return action, inp[2:]


if __name__ == '__main__':

	try : main(sys.argv[1:])
	except lib.error.MainException as e : print(e)
