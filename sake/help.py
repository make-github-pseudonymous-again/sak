# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import inspect, sake, lib.pacman, lib.check, functools, lib.source

def ensurefmt(fmt, n):
	fmt = list(fmt)
	if not fmt : fmt = [print,]
	while len(fmt) < n : fmt.append(fmt[-1])
	return tuple(fmt)


def walk(R, module, action, *fmt):

	fmtR, fmtM, fmtA = ensurefmt(fmt, 3)

	if module is None :
		print(fmtR(R))

	else :
		M = getattr(R, module, None)
		lib.check.ModuleDoesNotExistException(M, module, R)

		if action is None :
			print(fmtM(M))

		else :

			A = getattr(M, action, None)
			lib.check.ActionDoesNotExistException(A, action, M, module)

			print(fmtA(A))


def info(module = None, action = None):

	fmtR = functools.partial(lib.pacman.format, pred = inspect.ismodule)
	fmtM = functools.partial(lib.pacman.format, pred = inspect.isfunction)
	fmtA = lambda A : inspect.formatargspec(*inspect.getargspec(A))

	walk(sake, module, action, fmtR, fmtM, fmtA)


def doc(module = None, action = None):
	"""
		Print the doc of the specified element (default = sake root module)
	"""

	walk(sake, module, action, inspect.getdoc)


def source(module = None, action = None, linenos = False, filename = False):
	"""
		Print the source of the specified element (default = sake root module)
	"""

	fmt = functools.partial(lib.source.pretty, linenos = linenos, filename = filename)

	walk(sake, module, action, fmt)
