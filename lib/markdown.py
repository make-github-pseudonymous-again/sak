# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


def image ( title, img ) :
	return "![%s](%s)" % ( title, img )


def link ( text, href ) :
	return "[%s](%s)" % ( text, href )


def imagewithlink ( title, img, href ) :
	text = image( title, img )
	return link( text, href )
