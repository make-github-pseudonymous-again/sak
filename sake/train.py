from __future__ import absolute_import, division, print_function, unicode_literals

import sake.navigator

PROVIDER = "www.capitainetrain.com"

def search(fr, to, go, ret = None):
	query = "https://%s/search/%s/%s/%s" % (PROVIDER, fr, to, go)
	if ret is not None : query += "/%s" % ret
	sake.navigator.open(query)
