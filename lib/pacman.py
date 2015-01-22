
import inspect, lib, os, types

try :
	from importlib import import_module as importmodule
except :
	importmodule = __import__

def reset ( t ) :
	t.__all__ = []

def init ( t ) :
	if type( getattr( t , '__all__' , None ) ) != list :
		reset( t )

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


def resolve ( target, module ) :
	return lib.str.mostlikely( target, module.__all__ )


def __init__(t, root, ancestors = None):

	if ancestors is None :
		ancestors = [ ]

	uid = ancestors + [os.path.basename(root)]

	module = '.'.join( uid )

	_all = []

	for f in os.listdir(root):
		path = root + '/' + f

		if os.path.isdir(path):

			if f != '__pycache__' :

				if os.path.isfile( path + '/__init__.py' ) :
					child = importmodule( module + '.' + f )

				else :
					child = types.ModuleType( f )
					__init__( child , path , uid )

				setattr( t , f , child )
				_all.append( f )

		elif os.path.isfile(path) and f != '__init__.py':
			name, ext = os.path.splitext(f)

			if ext == '.py':
				s = importmodule(module + '.' + name)
				setattr(t, name, s)
				_all.append(name)
				toolbox(s)

	t.__all__ = _all

def format ( M , pred ) :
	return ', '.join( o for o , _ in inspect.getmembers( M , pred ) )
