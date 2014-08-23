import json, os.path, inspect


pretty = lambda *args, **kwargs : json.dump(*args, indent = '\t', separators=(',', ': '), **kwargs)

class proxy(object):

	def __init__(self, fname, mode = 'r', default = None, **kwargs):
		self.fname = fname
		self.data  = default if mode == 'r' or default is not None else {}
		self.mode  = mode
		self.kwargs = kwargs

	def __enter__(self):
		if os.path.exists(self.fname) :
			args = inspect.getargspec(json.load).args
			kwargs = { key : self.kwargs[key] for key in args if key in self.kwargs}
			with open(self.fname, 'r') as f : self.data = json.load(f, **kwargs)
		return self.data

	def __exit__(self, t, value, traceback):
		if self.mode == 'w':
			args = inspect.getargspec(json.dump).args
			kwargs = { key : self.kwargs[key] for key in args if key in self.kwargs}
			with open(self.fname, 'w') as f : pretty(self.data, f, **kwargs)