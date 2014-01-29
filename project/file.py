import hashlib

def checksum(f, h = hashlib.sha256(), blocksize = 2**15):
	chunk = f.read(blocksize)
	while len(chunk) > 0:
		h.update(chunk)
		chunk = f.read(blocksize)
	return h
