import lib.error, lib.list, lib.sys, inspect

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