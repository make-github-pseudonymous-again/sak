
import lib.inspect

def filter ( kwargs, fn ) :
	args = lib.inspect.getfullargspec(fn).args
	return dict( (key, kwargs[key]) for key in args if key in kwargs )
