
import json, os.path, inspect, lib.error, lib.kwargs, functools


pretty = functools.partial(json.dump, indent = '\t', separators = (',', ': '))

class proxy(object):

	def __init__(self, fname, mode = 'r', default = None, throws = False, **kwargs):
		self.fname = fname
		self.data  = default if mode == 'r' or default is not None else {}
		self.mode  = mode
		self.throws = throws
		self.kwargs = kwargs
		self.bytes = ""

	def backup(self):
		with open(self.fname, 'r') as f : self.bytes = f.read()

	def restore(self):
		with open(self.fname, 'w') as f : f.write(self.bytes)

	def load(self):
		kwargs = lib.kwargs.filter(self.kwargs, json.JSONDecoder)
		with open(self.fname, 'r') as f : self.data = json.load(f, **kwargs)

	def dump(self):
		kwargs = lib.kwargs.filter(self.kwargs, json.dump)
		with open(self.fname, 'w') as f : pretty(self.data, f, **kwargs)

	def __enter__(self):
		if os.path.exists(self.fname) :
			self.load()
			self.backup()
		elif self.throws :
			raise lib.error.FileDoesNotExist(self.fname)
		return self.data

	def __exit__(self, t, value, traceback):
		if self.mode == 'w':
			try : self.dump()
			except Exception as e :
				self.restore()
				raise e
