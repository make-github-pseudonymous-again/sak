from __future__ import absolute_import, division, print_function, unicode_literals

import urllib.parse, lib.http, lib.config

def resolve(resource, vendors):

	url = urllib.parse.urlparse(resource)

	p = list(url)

	if url.scheme == '' : p[0] = 'http'

	if url.netloc == '':
		found = False
		for domain, vendor in vendors.items():
			p[1] = domain
			if lib.http.access(urllib.parse.urlunparse(p)):
				found = True
				break

		if not found:
			return None

	
	user, _ = urllib.parse.splituser(p[1])
	if user is None:
		vendor = vendors[p[1]]
		user = lib.config.prompt_user(p[1], vendor.__name__)
		p[1] = user + '@' + p[1]

	return urllib.parse.urlunparse(p)