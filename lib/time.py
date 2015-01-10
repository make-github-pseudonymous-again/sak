
import time , datetime

def nanoseconds ( ) :
	return int( round( time.time( ) * 1e9 ) )

def parsedmy ( dmy ) :

	datefmt = "%d/%m/%Y"

	parsed = datetime.datetime.strptime( dmy , datefmt )

	timetuple = parsed.timetuple( )

	return time.mktime( timetuple ) * 1e9

def pretty ( timestamp ) :
	return datetime.datetime.utcfromtimestamp( timestamp / 1e9 ).strftime( "%Y-%m-%d %H:%M:%S" )
