import lib.error

def OptionNotInListException(key, value, available):
	if value not in available :
		raise lib.error.OptionNotInListException(key, value, available)