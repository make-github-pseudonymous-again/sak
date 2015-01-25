
import time

def callable(fn):
	return hasattr(fn, '__call__')


def val(o, *args, **kwargs):
	if callable(o) : return o(*args, **kwargs)
	else           : return o


def throttle ( times , interval ) :

	def wrap ( fn ) :

		count = 0
		first = time.perf_counter( )

		def wrapper ( *args , **kwargs ) :

			nonlocal count , first

			if count < times :

				count += 1

				fn( *args , **kwargs )

			else :

				now = time.perf_counter( )

				wait = interval - ( now - first )

				if wait <= 0 :

					count = 1

					first = now

					fn( *args , **kwargs )

				else :

					time.sleep( wait )

					wrapper( *args , **kwargs )

		return wrapper

	return wrap


