
import lib.http, lib.config

try :
	import urllib.parse as urlparse
	urllib = urlparse
except :
	import urlparse
	import urllib

def resolve(resource, vendors):

	url = urlparse.urlparse(resource)

	p = list(url)

	if url.scheme == '' : p[0] = 'http'

	if url.netloc == '':
		found = False
		for domain, vendor in vendors.items():
			p[1] = domain
			if lib.http.access(urlparse.urlunparse(p)):
				found = True
				break

		if not found:
			return None


	user, _ = urllib.splituser(p[1])
	if user is None:
		vendor = vendors[p[1]]
		user = lib.config.prompt_user(p[1], vendor.__name__)
		p[1] = user + '@' + p[1]

	return urlparse.urlunparse(p)
