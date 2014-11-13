# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import lib.git, lib.args, lib.json, lib.time, collections

def commit ( message, duration, authors = None ) :

	authors = lib.args.listify( authors )

	hook = collections.OrderedDict

	with lib.json.proxy( "contributions.json", mode = "w", default = [], object_pairs_hook = hook ) as contribs :

		contribs.append( hook( [

			( "authors", authors ),
			( "message", message ),
			( "duration", duration ),
			( "timestamp", str( lib.time.nanoseconds() ) )

		] ) )

	lib.git.add( "contributions.json" )
	lib.git.commit( "-m", message )
