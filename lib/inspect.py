
import inspect, sys

def inspectable ( fn ) :

	if inspect.isclass( fn ) :

		return fn.__init__

	else :

		return fn


def getargspec ( fn ) :

	fn = inspectable( fn )

	return inspect.getargspec( fn )
