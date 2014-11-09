# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os.path


def project ( directory ) :

	path = os.path.abspath( directory )
	name = os.path.basename( path )

	return path, name
