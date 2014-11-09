# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import lib.error, lib.list, lib.sys, inspect


def ModuleNameSpecified(root, inp):
	if len(inp) < 1:
		raise lib.error.ModuleNameNotSpecifiedException(root)

def ModuleNameExists(root, moduleName, modules):
	if len(modules) == 0:
		raise lib.error.ModuleDoesNotExistException(moduleName, root)

def ModuleNameNotAmbiguous(moduleName, modules):
	if len(modules) > 1:
		raise lib.error.ModuleNameAmbiguousException(moduleName, modules)

def ActionNameSpecified(inp, moduleName, module):
	if len(inp) < 2:
		raise lib.error.ActionNameNotSpecifiedException(module, moduleName)

def ActionNameExists(moduleName, module, actionName, actions):
	if len(actions) == 0:
		raise lib.error.ActionDoesNotExistException(actionName, module, moduleName)

def ActionNameNotAmbiguous(moduleName, module, actionName, actions):
	if len(actions) > 1:
		raise lib.error.ActionNameAmbiguousException(actionName, moduleName, actions)

def KwargsNotSupportedException( actionname, available ):
	if len( available ) == 0:
		raise lib.error.KwargsNotSupportedException( actionname )

def KwargNameExists( kwargname, actionname, matching, available ):
	if len( matching ) == 0:
		raise lib.error.KwargDoesNotExistException( kwargname, actionname, available )

def KwargNameNotAmbiguous( kwargname, actionname, matching ):
	if len( matching ) > 1:
		raise lib.error.KwargNameAmbiguousException( kwargname, actionname, matching )

def NotTooFewArgumentsForAction(moduleName, actionName, n, m, spec):
	if n < m:
		raise lib.error.TooFewArgumentsForActionException(n, spec, actionName, moduleName)

def NotTooManyArgumentsForAction(moduleName, actionName, n, m, spec):
	if spec[1] is None and n > len(spec[0]):
		raise lib.error.TooManyArgumentsForActionException(n, spec, actionName, moduleName)


def OptionNotInListException(key, value, available):
	if value not in available :
		raise lib.error.OptionNotInListException(key, value, available)

def SubprocessReturnedFalsyValueException(cmd, rc):
	if rc != 0 :
		raise lib.error.SubprocessReturnedFalsyValueException(cmd, rc)

def SubprocessOutputEmptyException(cmd, out):
	if out == b"" :
		raise lib.error.SubprocessOutputEmptyException(cmd)

def VersionNotUniqueException(versions):
	if not lib.list.one(versions.values()) :
		raise lib.error.VersionNotUniqueException(versions)

def CannotInferSemverVersionNumberException(old, version):
	if old is None :
		raise lib.error.CannotInferSemverVersionNumberException(version)

def SubprocessArgsEmptyException(args):
	if not args :
		raise lib.error.SubprocessArgsEmptyException()

def SubprocessExecutableNotFoundException(exe):
	if lib.sys.which(exe) is None :
		raise lib.error.SubprocessExecutableNotFoundException(exe)

def ActionDoesNotExistException(A, action, M, module):
	if A is None or not inspect.isfunction(A):
		raise lib.error.ActionDoesNotExistException(action, M, module)

def ModuleDoesNotExistException(M, module, parent):
	if M is None or not inspect.ismodule(M):
		raise lib.error.ModuleDoesNotExistException(module, parent)

def NoneValueException(key, value):
	if value is None :
		raise lib.error.NoneValueException(key)

def FalsyValueException(key, value):
	if not value :
		raise lib.error.FalsyValueException(key)

def NotNoneOrIntegerException(key, value):
	if value is None : return
	try : int(value)
	except : raise lib.error.NotNoneOrIntegerException(key)

try:

	import semantic_version

	def SemverVersionTagNotValidException(version):
		if not semantic_version.validate(version) :
			raise lib.error.SemverVersionTagNotValidException(version)

	def OldSemverVersionTagNotValidException(version, src):
		if not semantic_version.validate(version) :
			raise lib.error.OldSemverVersionTagNotValidException(version, src)

	def NewSemverVersionTagNotGreaterException(a, b):
		if not semantic_version.Version(a) > semantic_version.Version(b) :
			raise lib.error.NewSemverVersionTagNotGreaterException(a, b)

except ImportError as cause:

	e = lib.error.ModuleMissingException(cause, "semantic_version")

	SemverVersionTagNotValidException = lambda version : lib.error.throw(e)
	OldSemverVersionTagNotValidException = lambda version, src : lib.error.throw(e)
	NewSemverVersionTagNotGreaterException = lambda a, b : lib.error.throw(e)
