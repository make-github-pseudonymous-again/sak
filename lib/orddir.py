
import os, bisect


def split(item):
	x = 0

	for i, c in enumerate(item):

		if not c.isdigit() : break

		x *= 10
		x += int(c)

	return x, i


def read(cwd):
	d = {}
	w = 0
	for f in os.listdir(cwd):
		x, i = split(f)
		l = d.setdefault(x, [])
		v = f[i:]
		l.append((f, v))
		w = max(w, i)

	return d, w


def format(x, z):
	return ''.join(['{0:0', z, 'd}']).format(x)


def shift(d, n, beg = 0, end = None):

	out = []
	w = 0

	if len(d) == 0 or n == 0 : return out, w

	keys = sorted(d.keys())

	length = len(keys)

	if end is None : end = keys[-1] + 1

	i = bisect.bisect_left(keys, beg)

	while i < length:

		k = keys[i]
		if k >= end : break

		_k = str(k + n)
		l = d[k]
		out += [(f, _k + v) for f, v in l]

		w = max(w, len(_k))

		i += 1


	return out, w


def drange(where, beg, end):

	where = int(where)
	beg = int(beg)

	if end is not None : end = int(end)

	return where, beg, end

