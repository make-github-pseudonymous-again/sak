#!/usr/bin/python3

import sys, sake, inspect, lib.main, lib.pacman, lib.error


def main(inp):

	action, arguments = parse(inp)
	action(*arguments)


def parse(inp):

	# DETERMINE MODULE

	lib.main.checkModuleNameSpecified(sake, inp)
	moduleName = inp[0]

	modules = lib.pacman.resolve(moduleName, sake)

	lib.main.checkModuleNameExists(sake, moduleName, modules)
	lib.main.checkModuleNameNotAmbiguous(moduleName, modules)

	moduleName = modules[0]
	module = getattr(sake, moduleName)


	# DETERMINE ACTION

	lib.main.checkActionNameSpecified(inp, moduleName, module)
	actionName = inp[1]

	actions = lib.pacman.resolve(actionName, module)

	lib.main.checkActionNameExists(moduleName, module, actionName, actions)
	lib.main.checkActionNameNotAmbiguous(moduleName, module, actionName, actions)

	actionName = actions[0]
	action = getattr(module, actionName)


	# CHECK ACTION ARGUMENTS

	spec = inspect.getargspec(action)
	m = (0 if spec[0] is None else len(spec[0])) - (0 if spec[3] is None else len(spec[3]))
	n = len(inp) - 2

	lib.main.checkNotTooFewArgumentsForAction(moduleName, actionName, n, m, spec)
	lib.main.checkNotTooManyArgumentsForAction(moduleName, actionName, n, m, spec)


	# DONE
	return action, inp[2:]


if __name__ == '__main__':

	try : main(sys.argv[1:])
	except lib.error.MainException as e : print(e)
