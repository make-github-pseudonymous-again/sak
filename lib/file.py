import hashlib, sys, os

def hash(f, h = None, blocksize = 2**15):
	if h == None : h = hashlib.sha256()
	chunk = f.read(blocksize)
	while len(chunk) > 0:
		h.update(chunk)
		chunk = f.read(blocksize)
	return h


def walk(d):
	for e in sorted(os.listdir(d)):
		path = os.path.join(d, e)

		if   os.path.isdir(path)  : dcallback(path)
		elif os.path.isfile(path) : fcallback(path)
	