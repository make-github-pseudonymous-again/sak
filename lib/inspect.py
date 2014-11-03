# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import inspect, sys

def inspectable ( fn ) :

	if inspect.isclass( fn ) :

		return fn.__init__

	else :

		return fn


def getargspec ( fn ) :

	fn = inspectable( fn )

	return inspect.getargspec( fn )
