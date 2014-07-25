


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


except ImportError as e:

	_e = e

	def resolve(base, key):
		print(_e, ': to fix this --> pip3 install semantic_version')