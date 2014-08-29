from __future__ import absolute_import, division, print_function, unicode_literals

import json, os.path, inspect, lib.error, lib.kwargs


def pretty(*args, **kwargs) :
	json.dump(*args, indent = '\t', separators=(',', ': '), **kwargs)

class proxy(object):

	def __init__(self, fname, mode = 'r', default = None, throws = False, **kwargs):
		self.fname = fname
		self.data  = default if mode == 'r' or default is not None else {}
		self.mode  = mode
		self.throws = throws
		self.kwargs = kwargs

	def __enter__(self):
		if os.path.exists(self.fname) :
			kwargs = lib.kwargs.filter(self.kwargs, json.load)
			with open(self.fname, 'r') as f : self.data = json.load(f, **kwargs)
		elif self.throws :
			raise lib.error.FileDoesNotExist(self.fname)
		return self.data

	def __exit__(self, t, value, traceback):
		if self.mode == 'w':
			kwargs = lib.kwargs.filter(self.kwargs, json.dump)
			with open(self.fname, 'w') as f : pretty(self.data, f, **kwargs)