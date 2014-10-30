# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


def disjunction(predicates):
	return lambda x : True in (pred(x) for pred in predicates)
