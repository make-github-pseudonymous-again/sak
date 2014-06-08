import json


pretty = lambda *args : json.dump(*args, indent = '\t', separators=(',', ': '))

class proxy(object):

	def __init__(self, fname, mode = 'r'):
		self.fname = fname
		self.data  = None
		self.mode  = mode

	def __enter__(self):
		with open(self.fname, 'r') as f : self.data = json.load(f)
		return self.data

	def __exit__(self, t, value, traceback):
		if self.mode == 'w':
			with open(self.fname, 'w') as f : pretty(self.data, f)