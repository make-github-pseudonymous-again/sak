
from os import urandom
from random import seed , choice
import lib.args

@lib.args.convert( n = int )
def new ( n ) :

    seed( urandom( n ) )

    print( "".join( [ choice(
        "azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN`!$%%^&*()_+-=;,./<>?1234567890"
        ) for i in range( n ) ] ) )

@lib.args.convert( n = int )
def bytes ( n ) :

    print( " ".join( map( lambda x : hex( int( x ) )[2:] , urandom( n ) ) ) )

def hexadecimal ( password ) :

    print( " ".join(list(map(lambda x : hex( ord( x ) )[2:], password ) ) ) )
