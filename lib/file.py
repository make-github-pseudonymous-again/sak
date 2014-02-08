import hashlib, sys, os

def hash(f, h = None, blocksize = 2**15):
	if h == None : h = hashlib.sha256()
	chunk = f.read(blocksize)
	while len(chunk) > 0:
		h.update(chunk)
		chunk = f.read(blocksize)
	return h


def walk(s, d = None, f = print):
	if d is None : d = walk
	for e in sorted(os.listdir(s)):
		path = os.path.join(s, e)

		if   os.path.isdir(path)  : d(path)
		elif os.path.isfile(path) : f(path)
	