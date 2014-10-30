from __future__ import absolute_import, division, print_function, unicode_literals

import lib.sys, json

CMD_CURL = ["curl"]
FLAG_VERBOSE = ["-v"]
METHOD_PUT = "PUT"
METHOD_GET = "GET"
METHOD_POST = "POST"
METHOD_PATCH = "PATCH"
METHOD_UPDATE = "UPDATE"
METHOD_DELETE = "DELETE"

def body(data):
	if data is not None : return ["-d", data]
	else : return []

def resource(contenttype, location, url):
	if not location :  return ["-H", "Content-Type: %s" % contenttype, url]
	else : return ["-H", "Content-Type: %s" % contenttype, "-L", url]

def auth(username = None, password = None):
	if username is None : return []
	elif password is None : return ["-u", username]
	else : return ["-u", "%s:%s" % (username, password)]

def request(method):
	return ["-X", method]

def call(method, url, contenttype, data = None, username = None, password = None, location = False, **kwargs):

	cmd = []
	cmd.extend(CMD_CURL)
	cmd.extend(request(method))
	cmd.extend(FLAG_VERBOSE)
	cmd.extend(auth(username, password))
	cmd.extend(resource(contenttype, location, url))
	cmd.extend(body(data))

	return lib.sys.call(cmd, **kwargs)


def sendjson(method, url, data = None, username = None, password = None, **kwargs):
	if data is not None : data = json.dumps(data)
	return call(method, url, "application/json", data, username, password, **kwargs)

def putjson(url, data = None, username = None, password = None, **kwargs):
	return sendjson(METHOD_PUT, url, data, username, password, **kwargs)

def getjson(url, data = None, username = None, password = None, **kwargs):
	return sendjson(METHOD_GET, url, data, username, password, **kwargs)

def postjson(url, data = None, username = None, password = None, **kwargs):
	return sendjson(METHOD_POST, url, data, username, password, **kwargs)

def updatejson(url, data = None, username = None, password = None, **kwargs):
	return sendjson(METHOD_UPDATE, url, data, username, password, **kwargs)

def patchjson(url, data = None, username = None, password = None, **kwargs):
	return sendjson(METHOD_PATCH, url, data, username, password, **kwargs)

def deletejson(url, data = None, username = None, password = None, **kwargs):
	return sendjson(METHOD_DELETE, url, data, username, password, **kwargs)
