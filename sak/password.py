
from random import choice

def new ( ) :

    print( "".join( [ choice(
        "azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN`!$%%^&*()_+-=;,./<>?1234567890"
        ) for i in range( 8 ) ] ) )

def hexadecimal ( password ) :

    print( " ".join(list(map(lambda x : hex( ord( x ) )[2:], password ) ) ) )
