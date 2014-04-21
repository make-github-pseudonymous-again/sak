#!/usr/bin/python3

import sys, sake, inspect, lib


def main(inp):

	action, arguments = parse(inp)
	action(*arguments)


def parse(inp):
	# Determine module
	if len(inp) < 1:
		raise lib.error.ModuleNameNotSpecifiedException(sake)

	modules = lib.pacman.resolve(inp[0], sake)

	if len(modules) == 0:
		raise lib.error.ModuleDoesNotExistException(inp[0], sake)

	if len(modules) > 1:
		raise lib.error.ModuleNameAmbiguousException(inp[0], modules)

	inp[0] = modules[0]
	module = getattr(sake, inp[0])

	# Determine action
	if len(inp) < 2:
		raise lib.error.ActionNameNotSpecifiedException(module, inp[0])

	actions = lib.pacman.resolve(inp[1], module)

	if len(actions) == 0:
		raise lib.error.ActionDoesNotExistException(inp[1], module, inp[0])

	if len(actions) > 1:
		raise lib.error.ActionNameAmbiguousException(inp[1], inp[0], actions)

	inp[1] = actions[0]
	action = getattr(module, inp[1])

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
