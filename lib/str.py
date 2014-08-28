from __future__ import absolute_import, division, print_function, unicode_literals

import re

_v = 'aeiou'
_V = _v.upper()
_vV = _v + _V

_c = 'zrtypqsdfghjklmwxcvbn'
_C = _c.upper()
_cC = _c + _C


def filt(s, f):
	return ''.join([c for c in s if c in f])

vowe  = lambda s: filt(s, _vV)
cons  = lambda s: filt(s, _cC)
vowel = lambda s: filt(s, _v)
consl = lambda s: filt(s, _c)
voweu = lambda s: filt(s, _V)
consu = lambda s: filt(s, _C)


def natural(s):
	return [ int(c) if c.isdigit() else c for c in re.split('([0-9]+)', s) ]