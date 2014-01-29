import hashlib

def checksum(filename, h = hashlib.sha256(), blocksize = 2**15):
	with open(filename, 'rb') as f:
		chunk = f.read(blocksize)
		while len(chunk) > 0:
			h.update(chunk)
			chunk = f.read(blocksize)
	return h.digest()
