
import lib.queue

def stat ( ) :

	for key , val in lib.queue.stat( ) :

		print( key )


def submit ( name , cmd , nodes = None , cpu = None , output = None , error = None , walltime = None , memory = None , redirect = False ) :

	out , err , p = lib.queue.submit( name , cmd , nodes , cpu , output , error , walltime , memory , redirect )

	if out : print( out.decode() , end = "" )
	if err : print( err.decode() , end = "" )
