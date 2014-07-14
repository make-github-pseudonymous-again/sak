

def callable(fn):
	return hasattr(fn, '__call__')


def val(o, *args, **kwargs):
	if callable(o) : return o(*args, **kwargs)
	else           : return o