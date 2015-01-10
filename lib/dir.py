
import os, functools

def walk(s, d = None, f = print):
	"""
		Recursively walks a directory and applies different
		callback functions depending if the item is a file
		or a directory.
	"""
	if d is None : d = functools.partial(walk, d = d, f = f)
	for e in sorted(os.listdir(s)):
		path = os.path.join(s, e)

		if   d and os.path.isdir(path)  : d(path)
		elif f and os.path.isfile(path) : f(path)


def makedirs(*dirs):
	"""
		Creates all directories given by `dirs` as well as their parents.
	"""

	for d in dirs :
		if not os.path.exists(d) : os.makedirs(d)


def size(*dirs):
	"""
		Computes the size of a list of directories.
	"""
	# http://stackoverflow.com/a/1392549/1582182
	total_size = 0

	for d in dirs :
		for dirpath, dirnames, filenames in os.walk(d):
			for f in filenames:
				fp = os.path.join(dirpath, f)
				total_size += os.path.getsize(fp)

	return total_size


class cd (object) :

	"""
		http://stackoverflow.com/a/13197763/1582182
		Context manager for changing the current working directory
	"""

	def __init__(self, cwd):
		self.cwd = cwd

	def __enter__(self):
		self.old = os.getcwd()
		os.chdir(self.cwd)

	def __exit__(self, etype, value, traceback):
		os.chdir(self.old)
