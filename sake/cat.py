# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import functools, lib.file


def text ( filename, blocksize = 2 ** 15 ) :

	callback = functools.partial( print, end = "" )

	with open( filename ) as f :
		lib.file.read( f, callback, blocksize )
