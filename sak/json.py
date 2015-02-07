
import sys , lib.json , lib.args

def format ( *args , **kwargs ) :

	if args : lib.json.pretty( args , sys.stdout )
	if kwargs : lib.json.pretty( kwargs , sys.stdout )

def args ( files = None ) :

	files = lib.args.listify( files )

	for f in files :

		with lib.json.proxy( f ) as data :

			for key , val in data.items( ) :

				val = [ lib.args.escape( x ) for x in lib.args.listify( val ) ]
				val = " ".join( val )

				print( "--%s %s" % ( key , val ) , end = " " )

	print( )
