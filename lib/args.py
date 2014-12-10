# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import lib.json, itertools, lib.error

ARGS = "args"
KWARGS = "kwargs"
NO = "no"
DIRECTIVE_ARG = "+a"

def splitparts ( string , argv , i = 0 , j = None , eos = None , buf = "" , escapefirst = False ) :

	"""
		Splits a command line argument string into tokens. Tokens are separated by whitespace. Whitespace can be included inside tokens
		by wrapping tokens with single or double quotes. Whitespace can also be included by escaping them without the need for quote wrapping.
		When inside a string standard escape sequence are allowed : line-feed and tabulations for example.
		This method will return a tuple that can be used to continue the analysis of a string that was incomplete the first time the method was run.
	"""

	if j == None :
		j = len( string )

	if escapefirst and i < j :
		buf += string[i]
		i += 1

	while i < j :

		c = string[i]

		if c == '\\' :
			# escaped character
			i += 1

			if i == j :
				return eos , buf , True

			buf += string[i]

		elif eos is None and c == ' ' :
			if buf :
				argv.append( buf )
				buf = ""

		elif c == '\'' or c == '"' :
			if eos is None :
				# beginning of a new string
				eos = c
			elif c == eos :
				# this is the end of the current string
				eos = None
			else :
				# this is simply an quote character
				buf += c

		else :
			buf += c

		i += 1

	return eos , buf , False


def split ( string ) :

	argv = []

	eos , buf , escaped = splitparts( string , argv )

	if eos is not None:
		raise Exception( "could not split arguments : incomplete string" )

	elif escaped :
		raise Exception( "could not split arguments : trailing escape char" )

	if buf :
		argv.append( buf )

	return argv


def parse ( argv, args, kwargs ) :

	"""

		>>> from lib.args import *

		>>> parse( ["a", "b", "c", "--flag"], [], {} )
		(['a', 'b', 'c'], {'flag': True})

	"""

	key = ""
	isflag = False
	isvalue = False
	islist = False
	isarg = False

	for p in argv:

		if isarg : args.append(p)

		elif p == DIRECTIVE_ARG : isarg = True

		elif len(p) > 1 and p[0] == '-' and not p[1].isdigit():
			isvalue = False
			isflag = False
			islist = False
			if p[1] == '-':
				p = p[2:]

				if len(p) == 0 : continue

				v = True
				if len(p) > 1 and p[:2] == NO :
					v = False
					p = p[2:]

				kwargs[p] = v
				key = p
				isflag = True

			elif len(p) == 2:

				p = p[1]

				kwargs[p] = True
				key = p
				isflag = True

			else:
				for c in p[1:] : kwargs[c] = True

		else :
			if isflag :
				isflag = False
				isvalue = True
				kwargs[key] = p
			elif isvalue :
				isvalue = False
				islist = True
				kwargs[key] = [kwargs[key], p]
			elif islist : kwargs[key].append(p);
			else : args.append(p)

	return args, kwargs


def format ( key, val ) :

	"""

		>>> from lib.args import *

		>>> format( 'filter', 'false' )
		'--filter=false'

		>>> format( 'i', 'input.json' )
		'-i=input.json'

	"""

	fmt = "-%s=%s"

	if len(key) > 1 : fmt = "-" + fmt

	return fmt % (key, val)


def listify ( arg ) :

	"""

		>>> from lib.args import *

		>>> listify( None )
		[]

		>>> listify( 'value' )
		['value']

		>>> listify( ['value1', 'value2'] )
		['value1', 'value2']

	"""

	if arg is None :
		return []
	elif isinstance( arg, str ) :
		return [ arg ]
	else :
		return arg


def kwargslist( spec ) :

	out = []

	if spec.args is not None and spec.defaults is not None :
		out.extend( spec.args[-len( spec.defaults ):] )

	if spec.varargs is not None :
		out.append( spec.varargs )

	if spec.keywords is not None :
		out.append( spec.keywords )

	return out



def inflate ( args, kwargs ) :
	"""
		Loads more arguments if JSON ARGS or KWARGS source have been specified.
		Since JSON KWARGS could contain more ARGS or KWARGS directives
		the inflate operations loops until no JSON source is specified anymore.
		The last JSON source that is read will always serve as a
		base and thus JSON files referencing other JSON files are inheriting the
		properties of those other JSON files. Similarly, JSON ARGS will be prepended to the
		existing argument list.

		/!\ Currently only support one kwargs json file argument
	"""

	jsonargssources = []

	while True :

		if ARGS in kwargs :
			if not isinstance(kwargs[ARGS], list) : kwargs[ARGS] = [kwargs[ARGS]]
			jsonargssources[:0] = kwargs[ARGS]
			del kwargs[ARGS]

		if not KWARGS in kwargs : break

		source = kwargs[KWARGS]
		del kwargs[KWARGS]

		kwargscopy = dict(kwargs)
		kwargs.clear()

		with lib.json.proxy(source, throws = True) as data : kwargs.update(data)

		kwargs.update(kwargscopy)


	argscopy = list(args)
	del args[:]

	for source in jsonargssources :
		with lib.json.proxy(source, throws = True) as data : args.extend(data)

	args.extend(argscopy)


def validate ( handle = print, **predicates ) :

	"""

		>>> from lib.args import *

		>>> @validate( a = lambda v : v <= 13 , b = lambda v : len(v) > 0, c = lambda v : v[:2] == "ab" )
		... def test ( a, b = None, c = None ) :
		... 	print( 'ok' )

		>>> test ( 13, c = 'abdf', b = [1] )
		ok

		>>> test ( 13.2, c = 'abdf', b = [1,2] )
		cannot validate arg 'a' = 13.2
		ok

		>>> test ( 13, c = 'df' )
		cannot validate arg 'c' = 'df'
		ok

	"""

	def wrap ( fn ) :

		def wrapper( *args, **kwargs ) :

			argkeys = fn.__code__.co_varnames

			argpairs = ( ( argkeys[i], v ) for i, v in enumerate( args ) )
			kwargpairs = kwargs.items()

			fmt = "cannot validate arg '%s' = %r"

			for k, v in itertools.chain( argpairs, kwargpairs ) :

				if k in predicates and not predicates[k](v) :
					handle( fmt % ( k , v ) )

			return fn( *args, **kwargs )

		wrapper.__name__ = fn.__name__
		return wrapper

	return wrap

def accepts ( handle = print, **types ) :

	"""

		>>> from lib.args import *

		>>> @accepts( a = int, b = list, c = str )
		... def test ( a, b = None, c = None ) :
		... 	print( 'ok' )

		>>> test ( 13, c = 'df', b = [] )
		ok

		>>> test ( 13.2, c = 'df', b = [] )
		arg 'a' = 13.2 does not match <class 'int'>
		ok

		>>> test ( 13, c = 'df' )
		ok

	"""

	def wrap ( fn ) :

		def wrapper( *args, **kwargs ) :

			argkeys = fn.__code__.co_varnames

			argpairs = ( ( argkeys[i], v ) for i, v in enumerate( args ) )
			kwargpairs = kwargs.items()

			fmt = "arg '%s' = %r does not match %s"

			for k, v in itertools.chain( argpairs, kwargpairs ) :

				if k in types and not isinstance( v, types[k] ) :
					handle( fmt % ( k, v, types[k] ) )

			return fn( *args, **kwargs )

		wrapper.__name__ = fn.__name__
		return wrapper

	return wrap


def convert ( handle = lambda msg : lib.error.throw( Exception( msg ) ), **convertors ) :

	"""

		>>> from lib.args import *

		>>> @convert( print, a = int, b = list, c = str )
		... def test ( a, b = list("abc"), c = "2" ) :
		... 	print( [a , b , c] )

		>>> test ( "13", c = 5, b = "123" )
		[13, ['1', '2', '3'], '5']

		>>> test ( 13.2, c = 'df', b = (1,) )
		[13, [1], 'df']

		>>> test ( 13, c = 'df' )
		[13, ['a', 'b', 'c'], 'df']

		>>> test ( 13, 1, c = 'df' )
		error in the conversion of arg 'b' = 1 using <class 'list'>, the error is 'int' object is not iterable
		[13, 1, 'df']

	"""

	def wrap ( fn ) :

		def wrapper( *args, **kwargs ) :

			argkeys = fn.__code__.co_varnames

			argpairs = ( ( i, argkeys[i], v ) for i, v in enumerate( args ) )
			kwargpairs = ( ( k , k , v ) for k , v in kwargs.items() )
			m = len ( args )
			n = len ( kwargs )

			fmt = "error in the conversion of arg '%s' = %r using %s, the error is %s"

			args = list( args )
			kwargs = dict( kwargs )

			for a, ikv in zip( itertools.chain( itertools.repeat(args, m ), itertools.repeat(kwargs, n) ),  itertools.chain( argpairs, kwargpairs ) ) :

				i, k, v = ikv

				if k in convertors :
					try :
						 a[i] = convertors[k]( v )
					except Exception as e:
						handle( fmt % ( k, v, convertors[k], e ) )

			return fn( *args, **kwargs )

		wrapper.__name__ = fn.__name__
		return wrapper

	return wrap
