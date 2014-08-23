import lib.error, lib.list

def OptionNotInListException(key, value, available):
	if value not in available :
		raise lib.error.OptionNotInListException(key, value, available)

def SubprocessReturnedFalsyValueException(cmd, rc):
	if rc != 0 :
		raise lib.error.SubprocessReturnedFalsyValueException(cmd, rc)

def VersionNotUniqueException(versions):
	if not lib.list.one(versions.values()) :
		raise lib.error.VersionNotUniqueException(versions)

def CannotInferSemverVersionNumberException(old, version):
	if old is None :
		raise lib.error.CannotInferSemverVersionNumberException(version)

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