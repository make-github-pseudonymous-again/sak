


def sentinel(n, a, b = None):
	for i in range(n - 1) : yield a
	yield b


def attribute ( iterable , attrname ) :

	for item in iterable : yield item[attrname]
