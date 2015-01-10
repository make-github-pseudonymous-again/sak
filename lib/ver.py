
import lib.error

PREFIX = 'v'
KEYS = ['major', 'minor', 'patch']

try:

	import semantic_version

	def resolve(base, key):
		v = semantic_version.Version(base)
		setattr(v, key, getattr(v, key) + 1)
		i = KEYS.index(key) + 1
		for k in KEYS[i:] : setattr(v, k, 0)
		return str(v)


except ImportError as cause:

	e = lib.error.ModuleMissingException(cause, "semantic_version")

	resolve = lambda base, key : lib.error.throw(e)


def isspecial(v):
	return v in KEYS
