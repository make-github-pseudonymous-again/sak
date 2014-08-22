
import lib.error

PREFIX = 'v'
KEYS = ['major', 'minor', 'patch']

try:

	import semantic_version

	def resolve(base, key):
		v = semantic_version.Version(base)
		setattr(v, key, getattr(v, key) + 1)
		start = KEYS.index(key) + 1
		for i in range(start, len(KEYS)) : setattr(v, KEYS[i], 0)
		return str(v)


except ImportError as cause:

	e = lib.error.ModuleMissingException(cause, "semantic_version")

	resolve = lambda base, key : lib.error.throw(e)