from __future__ import absolute_import, division, print_function, unicode_literals






def one(iterator):
	try:
		iterator = iter(iterator)
		first = next(iterator)
		return all(first == rest for rest in iterator)
	except StopIteration:
		return True