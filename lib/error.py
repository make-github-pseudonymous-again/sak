import inspect, lib.pacman, json


def throw(e):
	raise e

class MainException(Exception):
	def __init__(self, what):
		Exception.__init__(self, what)

	def what(self):
		return self.args[0]

	def __repr__(self):
		return self.what()


class ModuleNameNotSpecifiedException(MainException):
	def __init__(self, main_module):
		fmt = 'Module name not specified, available modules are : %s'
		args = (', '.join(sorted(lib.pacman.public(main_module, [inspect.ismodule]))))
		MainException.__init__(self, fmt % args)

class ModuleNameAmbiguousException(MainException):
	def __init__(self, module_name, l):
		fmt = 'Module \'%s\' is ambiguous, matching modules are : %s'
		args = (module_name, ', '.join(l))
		MainException.__init__(self, fmt % args)

class ModuleDoesNotExistException(MainException):
	def __init__(self, module_name, main_module):
		fmt = 'Module \'%s\' does not exist, available modules are : %s'
		args = (module_name, ', '.join(sorted(lib.pacman.public(main_module, [inspect.ismodule]))))
		MainException.__init__(self, fmt % args)

class ActionNameNotSpecifiedException(MainException):
	def __init__(self, module, module_name):
		fmt = 'Action name in module \'%s\' not specified, available actions are : %s'
		args = (module_name, ', '.join(sorted(lib.pacman.public(module, [inspect.isfunction]))))
		MainException.__init__(self, fmt % args)

class ActionNameAmbiguousException(MainException):
	def __init__(self, action_name, module_name, l):
		fmt = 'Action \'%s\' in module \'%s\' is ambiguous, matching actions are : %s'
		args = (action_name, module_name, ', '.join(l))
		MainException.__init__(self, fmt % args)

class ActionDoesNotExistException(MainException):
	def __init__(self, action_name, module, module_name):
		fmt = 'Action \'%s\' in module \'%s\' does not exist, available actions are : %s'
		args = (action_name, module_name, ', '.join(sorted(lib.pacman.public(module, [inspect.isfunction]))))
		MainException.__init__(self, fmt % args)

class TooFewArgumentsForActionException(MainException):
	def __init__(self, n, spec, action_name, module_name):
		fmt = 'Too few arguments for action \'%s\' in module \'%s\', signature is %s, got %d'
		args = (action_name, module_name, inspect.formatargspec(*spec), n)
		MainException.__init__(self, fmt % args)

class TooManyArgumentsForActionException(MainException):
	def __init__(self, n, spec, action_name, module_name):
		fmt = 'Too many arguments for action \'%s\' in module \'%s\', signature is %s, got %d'
		args = (action_name, module_name, inspect.formatargspec(*spec), n)
		MainException.__init__(self, fmt % args)


class OptionNotInListException(MainException):
	def __init__(self, key, value, available):
		fmt = "%s '%s' is not valid, should be in %s"
		args = (key, value, json.dumps(available))
		MainException.__init__(self, fmt % args)


class SubprocessReturnedFalsyValueException(MainException):
	def __init__(self, cmd, rc):
		fmt = "subprocess '%s' exited with return code %d"
		args = (" ".join(cmd), rc)
		MainException.__init__(self, fmt % args)

class SemverVersionTagNotValidException(MainException):
	def __init__(self, version):
		fmt = "version tag '%s' not valid (http://semver.org/)"
		args = version
		MainException.__init__(self, fmt % args)

class OldSemverVersionTagNotValidException(MainException):
	def __init__(self, version, src):
		fmt = "old version tag '%s' in '%s' not valid (http://semver.org/)"
		args = (version, src)
		MainException.__init__(self, fmt % args)

class NewSemverVersionTagNotGreaterException(MainException):
	def __init__(self, a, b):
		fmt = "version tag '%s' should be > than '%s'"
		args = (a, b)
		MainException.__init__(self, fmt % args)

		

class ModuleMissingException(MainException):
	def __init__(self, cause, name):
		fmt = "'%s' : to fix this --> pip3 install %s"
		args = (cause, name)
		MainException.__init__(self, fmt % args)
		
		