import lib.orddir, lib.file


def read(cwd = '.'):
	d = lib.orddir.read(cwd)
	print(d)


def move(item, where, cwd = '.'):
	beg = int(item)
	end = beg + 1
	shift(where, beg, end, cwd)


def zfill(z, cwd = '.'):
	d = lib.orddir.read(cwd)
	mv = []
	for k, l in d.items():
		_k = lib.orddir.format(k, z)
		mv += [(f, _k + v) for f, v in l]

	lib.file.move(mv, cwd)


def shift(where, beg = '0', end = None, cwd = '.'):

	where, beg, end = lib.orddir.drange(where, beg, end)
	d = lib.orddir.read(cwd)
	n = where - beg
	mv = lib.orddir.shift(d, n, beg, end)
	lib.file.move(mv, cwd)