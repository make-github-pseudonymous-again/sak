

def disjunction(predicates):
	return lambda x : True in (pred(x) for pred in predicates)
