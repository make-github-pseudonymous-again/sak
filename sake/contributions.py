# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import lib.git, lib.args, lib.json, lib.time

def commit ( message, duration, authors = None ) :

	authors = lib.args.listify( authors )

	lib.git.commit( "-m", message )

	with lib.json.proxy( "contributions.json", mode = "w", default = [] ) as contribs :

		contribs.append( {

			"authors" : authors,
			"message" : message,
			"duration" : duration,
			"timestamp" : lib.time.nanoseconds()

		} )

