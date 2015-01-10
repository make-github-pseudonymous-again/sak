import sak.navigator

PROVIDER = "www.capitainetrain.com"

def search(fr, to, go, ret = None):
	query = "https://%s/search/%s/%s/%s" % (PROVIDER, fr, to, go)
	if ret is not None : query += "/%s" % ret
	sak.navigator.open(query)
