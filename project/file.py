import hashlib

def checksum(f, h = None, blocksize = 2**15):
	if h == None : h = hashlib.sha256()
	chunk = f.read(blocksize)
	while len(chunk) > 0:
		h.update(chunk)
		chunk = f.read(blocksize)
	return h
