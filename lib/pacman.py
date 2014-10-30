# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import inspect, lib, os, types

try :
	from importlib import import_module as importmodule
except :
	importmodule = __import__

def reset(t):
	t.__all__ = []

def init(t):
	if type(getattr(t, '__all__', None)) != list:
		reset(t)

def exists(s, t):
	return s in t.__dict__

def public(t, pred = None):
	if pred is None : pred = []

	if len(pred) == 0:
		for key in t.__all__ :
			yield key

	for key in t.__all__:
		for p in pred:
			if p(getattr(t, key)):
				yield key
				break

def setpublic(t, pred = None):
	if pred is None : pred = []

	if len(pred) == 0 :
		t.__all__ = t.__dict__.keys()
		return

	publ = set(t.__all__)
	for key, val in t.__dict__.items():
		if key in publ : continue
		for p in pred :
			if p(val):
				publ.add(key)
				break



	t.__all__ = list(publ)

def ispublic(s, t):
	return s in t.__all__


def setprivate(t, pred = None):
	if pred is None : pred = []

	if len(pred) == 0:
		t.__all__ = []
		return


	publ = set(t.__all__)

	for key in t.__all__:
		for p in pred :
			if p(getattr(t, key)):
				publ.remove(key)
				break

	t.__all__ = list(publ)

def isprivate(s, t):
	return exists(s, t) and not ispublic(s, t)


def clean(t):
	publ = set(t.__all__)
	for key in t.__all__:
		try:
			getattr(t, key)
		except AttributeError:
			publ.remove(key)

	t.__all__ = list(publ)


def package(t):
	reset(t)
	setpublic(t, [inspect.ismodule])

def module(t):
	package(t)
	setpublic(t, [inspect.isclass, inspect.isfunction, inspect.isgenerator])

def toolbox(t):
	reset(t)
	setpublic(t, [inspect.isfunction])


NAME_RESOLVER = [
	# MATCH
	lambda t, a, s : [x for x in t.__all__ if a(x) == s],
	# PREFIX
	lambda t, a, s : [x for x in t.__all__ if a(x).startswith(s)],
	# SUFFIX
	lambda t, a, s : [x for x in t.__all__ if a(x).endswith(s)],
	# SUBSTR
	lambda t, a, s : [x for x in t.__all__ if s in a(x)]
]


NAME_TRANSFORMER = [
	lambda s : s,
	lambda s : s.lower(),
	lambda s : lib.str.cons(s),
	lambda s : lib.str.cons(s.lower())
]

def resolve(n, t):

	for a in NAME_TRANSFORMER:
		s = a(n)

		for r in NAME_RESOLVER:
			l = r(t, a, s)

			if len(l) > 0 :
				return l

	return []



def __init__(t, root):

	reset(t)

	module = os.path.basename(root)

	for f in os.listdir(root):
		path = root + '/' + f

		if os.path.isdir(path):
			if os.path.isfile(path + '/__init__.py'):
				setattr(t, f, importmodule(module + '.' + f))
				t.__all__.append(f)

			elif f != '__pycache__':
				setattr(t, f, types.ModuleType(f))
				__init__(t, path)

		elif os.path.isfile(path) and f != '__init__.py':
			name, ext = os.path.splitext(f)

			if ext == '.py':
				s = importmodule(module + '.' + name)
				setattr(t, name, s)
				t.__all__.append(name)
				toolbox(s)

def format(M, pred):
	return ', '.join(o for o, _ in inspect.getmembers(M, pred))
