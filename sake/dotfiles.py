# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import lib.git

def vimbundle ( url ) :

	repo = url.split("/")[-1]

	lib.git.submodule( "add" , url, ".vim/bundle/%s" % repo )
