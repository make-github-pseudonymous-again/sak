from __future__ import absolute_import, division, print_function, unicode_literals


import lib.error

def checkModuleNameSpecified(root, inp):
	if len(inp) < 1:
		raise lib.error.ModuleNameNotSpecifiedException(root)

def checkModuleNameExists(root, moduleName, modules):
	if len(modules) == 0:
		raise lib.error.ModuleDoesNotExistException(moduleName, root)

def checkModuleNameNotAmbiguous(moduleName, modules):
	if len(modules) > 1:
		raise lib.error.ModuleNameAmbiguousException(moduleName, modules)

def checkActionNameSpecified(inp, moduleName, module):
	if len(inp) < 2:
		raise lib.error.ActionNameNotSpecifiedException(module, moduleName)

def checkActionNameExists(moduleName, module, actionName, actions):
	if len(actions) == 0:
		raise lib.error.ActionDoesNotExistException(actionName, module, moduleName)

def checkActionNameNotAmbiguous(moduleName, module, actionName, actions):
	if len(actions) > 1:
		raise lib.error.ActionNameAmbiguousException(actionName, moduleName, actions)

def checkNotTooFewArgumentsForAction(moduleName, actionName, n, m, spec):
	if n < m:
		raise lib.error.TooFewArgumentsForActionException(n, spec, actionName, moduleName)

def checkNotTooManyArgumentsForAction(moduleName, actionName, n, m, spec):
	if spec[1] is None and n > len(spec[0]):
		raise lib.error.TooManyArgumentsForActionException(n, spec, actionName, moduleName)
