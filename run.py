#!/usr/bin/python3

import sys, project, inspect, json


def main(arg):

	if len(arg) < 1 : raise project.error.MainException('Module name not specified, available modules are %s' % (json.dumps([ o for o, _ in inspect.getmembers(project, inspect.ismodule)])))
	module = getattr(project, arg[0], None)
	if module == None or not inspect.ismodule(module): raise project.error.MainException('Module \'%s\' does not exist, available modules are %s' % (arg[0], json.dumps([ o for o, _ in inspect.getmembers(project, inspect.ismodule)])))

	if len(arg) < 2 : raise project.error.MainException('Action name in module \'%s\' not specified, available actions are %s' % (arg[0], json.dumps([ o for o, _ in inspect.getmembers(module, inspect.isfunction)])))
	action = getattr(module, arg[1], None)
	if action == None or not inspect.isfunction(action): raise project.error.MainException('Action \'%s\' in module \'%s\' does not exist, available actions are %s' % (arg[1], arg[0], json.dumps([ o for o, _ in inspect.getmembers(module, inspect.isfunction)])))

	spec = inspect.getargspec(action)
	m = (0 if spec[0] == None else len(spec[0])) - (0 if spec[3] == None else len(spec[3]))
	n = len(arg) - 2
	if n < m : raise project.error.MainException('Too few arguments for action \'%s\' in module \'%s\', signature is %s, got %d' % (arg[1], arg[0], inspect.formatargspec(*spec), n))
	if spec[1] == None and n > len(spec[0]) : raise project.error.MainException('Too many arguments for action \'%s\' in module \'%s\', signature is %s, got %d' % (arg[1], arg[0], inspect.formatargspec(*spec), n))
	action(*arg[2:])


if __name__ == '__main__':

	try : main(sys.argv[1:])
	except project.error.MainException as e : print(e.what())
