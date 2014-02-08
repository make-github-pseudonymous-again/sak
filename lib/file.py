import hashlib, sys, os, lib.dir


def read(f, callback, blocksize = 2**15):
	chunk = f.read(blocksize)
	while len(chunk) > 0:
		callback(chunk)
		chunk = f.read(blocksize)

def hash(f, h = None, blocksize = 2**15):
	if h == None : h = hashlib.sha256()
	read(f, h.update, blocksize)
	return h

def walk(src, f):

	def callback(path):
		with open(path, 'r') as g : f(g)

	lib.dir.walk(src, f = callback)
	