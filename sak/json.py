
import sys , lib.json

def format ( *args , **kwargs ) :

	if args : lib.json.pretty( args , sys.stdout )
	if kwargs : lib.json.pretty( kwargs , sys.stdout )
