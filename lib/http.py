import urllib.parse, http.client

def access(url):
	p = urllib.parse.urlparse(url)
	conn = http.client.HTTPConnection(p.netloc)
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