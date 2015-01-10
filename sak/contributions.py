import lib.git, lib.args, lib.json, lib.time, collections

def commit ( message, duration, authors = None ) :

	authors = lib.args.listify( authors )

	hook = collections.OrderedDict

	with lib.json.proxy( "contributions.json", mode = "w", default = [], object_pairs_hook = hook ) as contribs :

		contribs.append( hook( [

			( "authors", authors ),
			( "message", message ),
			( "duration", duration ),
			( "timestamp", str( lib.time.nanoseconds( ) ) )

		] ) )

	lib.git.add( "contributions.json" )
	lib.git.commit( "-m", message )


def manhours ( begin = None , end = None ) :

	if begin is None :
		begin = 0
	else :
		begin = lib.time.parsedmy( begin )

	if end is None :
		end = lib.time.nanoseconds( )
	else :
		end = lib.time.parsedmy( end )

	total = 0

	with lib.json.proxy( "contributions.json", mode = "r", default = [] ) as contribs :

		for contrib in contribs :

			t = int( contrib["timestamp"] )

			if t >= begin and t <= end :

				total += int( contrib["duration"] ) * len( contrib["authors"] )

	print( total )


def log ( begin = None , end = None ) :

	if begin is None :
		begin = 0
	else :
		begin = lib.time.parsedmy( begin )

	if end is None :
		end = lib.time.nanoseconds( )
	else :
		end = lib.time.parsedmy( end )

	with lib.json.proxy( "contributions.json", mode = "r", default = [] ) as contribs :

		for contrib in contribs :

			t = int( contrib["timestamp"] )

			if t >= begin and t <= end :

				authors = contrib["authors"]
				duration = contrib["duration"]

				print( lib.time.pretty( t ) , "~" , " , ".join( authors ) , "(" , duration , ")" )
				print( " ->" , contrib["message"] )
				print( "===" )
