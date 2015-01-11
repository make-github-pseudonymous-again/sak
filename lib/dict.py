
def one ( iterator ) :

	try :
		iterator = iter( iterator )
		_ , first = next( iterator )
		return all( first == rest for _ , rest in iterator )

	except StopIteration :
		return True


def select ( source , keys ) :

	return { key : source[key] for key in keys if key in source }
