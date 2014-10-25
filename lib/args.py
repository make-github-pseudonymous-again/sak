from __future__ import absolute_import, division, print_function, unicode_literals

import lib.json

ARGS = "args"
KWARGS = "kwargs"
NO = "no"
DIRECTIVE_ARG = "+a"

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


def format(key, val):

	fmt = "-%s=%s"

	if len(key) > 1 : fmt = "-" + fmt

	return fmt % (key, val)


def inflate(args, kwargs):
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
