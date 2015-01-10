

def disjunction ( predicates ) :
	return lambda x : any( pred( x ) for pred in predicates )
