

def get ( **kwargs ) :

	return "?" + "&".join( map( "=".join, kwargs.items() ) )
