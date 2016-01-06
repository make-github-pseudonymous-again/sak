
import inspect
import sys


def inspectable(fn):

    if inspect.isclass(fn):

        return fn.__init__

    else:

        return fn


def getfullargspec(fn):

    fn = inspectable(fn)

    return inspect.getfullargspec(fn)
