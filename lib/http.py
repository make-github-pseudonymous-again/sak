

try :
	import http.client as httplib
except :
	import httplib

try :
	import urllib.parse as urlparse
except :
	import urlparse

def access(url):
	p = urlparse.urlparse(url)
	conn = httplib.HTTPConnection(p.netloc)
	conn.request('HEAD', p.path)
	resp = conn.getresponse()
	return resp.status < 400


def url(domain, path = None, username = None, secure = False):

	fmt = "http"
	args = []

	if secure : fmt += "s"

	fmt += "://%s"

	if username is not None :
		fmt += "@%s"
		args.append(username)

	args.append(domain)

	if path is not None:
		fmt += "/%s"
		args.append(path)

	return fmt % tuple(args)
