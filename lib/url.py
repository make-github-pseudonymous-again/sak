# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


def get ( **kwargs ) :

	return "?" + "&".join( map( "=".join, kwargs.items() ) )
