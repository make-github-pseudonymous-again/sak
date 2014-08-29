#!/usr/bin/python3
from __future__ import absolute_import, division, print_function, unicode_literals


import sys, sake, inspect, lib.pacman, lib.error, lib.check, lib.args


def main(inp):

	action, args = parse(inp)
	args, kwargs = lib.args.parse(args, [], {})
	lib.args.inflate(args, kwargs)
	action(*args, **kwargs)


def parse(inp):

	# DETERMINE MODULE

	lib.check.ModuleNameSpecified(sake, inp)
	moduleName = inp[0]

	modules = lib.pacman.resolve(moduleName, sake)

	lib.check.ModuleNameExists(sake, moduleName, modules)
	lib.check.ModuleNameNotAmbiguous(moduleName, modules)

	moduleName = modules[0]
	module = getattr(sake, moduleName)


	# DETERMINE ACTION

	lib.check.ActionNameSpecified(inp, moduleName, module)
	actionName = inp[1]

	actions = lib.pacman.resolve(actionName, module)

	lib.check.ActionNameExists(moduleName, module, actionName, actions)
	lib.check.ActionNameNotAmbiguous(moduleName, module, actionName, actions)

	actionName = actions[0]
	action = getattr(module, actionName)


	# CHECK ACTION ARGUMENTS

	spec = inspect.getargspec(action)
	m = (0 if spec[0] is None else len(spec[0])) - (0 if spec[3] is None else len(spec[3]))
	n = len(inp) - 2

	lib.check.NotTooFewArgumentsForAction(moduleName, actionName, n, m, spec)
	lib.check.NotTooManyArgumentsForAction(moduleName, actionName, n, m, spec)


	# DONE
	return action, inp[2:]


if __name__ == '__main__':

	try : main(sys.argv[1:])
	except lib.error.MainException as e : print(e)
