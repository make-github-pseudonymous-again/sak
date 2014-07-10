import urllib.parse, http.client

def access(url):
	p = urllib.parse.urlparse(url)
	conn = http.client.HTTPConnection(p.netloc)
	conn.request('HEAD', p.path)
	resp = conn.getresponse()
	return resp.status < 400