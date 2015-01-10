import lib.error, lib.url

SPOOF_USER_AGENT = "Mozilla/5.0 (X11; U; Linux x86_64; fr; rv:1.9.1.5) Gecko/20091109 Ubuntu/9.10 (karmic) Firefox/3.5.5"

try:

	import lxml.etree

	try :
		import urllib.request as urllib2
	except :
		import urllib2


	def title ( url, *args ) :
		request = urllib2.Request(url)
		request.add_header("User-Agent", SPOOF_USER_AGENT)
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor)
		conn = opener.open(request)
		parser = lxml.etree.HTMLParser(encoding = "utf-8")
		tree = lxml.etree.parse(conn, parser = parser)
		title = tree.find('.//title')
		if title is not None : text = title.text
		else : text = url

		print ( text )

		if len(args) : href(*args)


	def href(url, *args):
		request = urllib2.Request(url)
		request.add_header("User-Agent", SPOOF_USER_AGENT)
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor)
		conn = opener.open(request)
		parser = lxml.etree.HTMLParser(encoding = "utf-8")
		tree = lxml.etree.parse(conn, parser = parser)
		title = tree.find('.//title')
		if title is not None : text = title.text
		else : text = url
		fmt = '<a href="%s">%s</a>'
		print(fmt % (url, text))

		if len(args) : href(*args)

except ImportError as cause:

	e = lib.error.ModuleMissingException(cause, "lxml")

	title = lambda url, *args : lib.error.throw(e)
	href = lambda url, *args : lib.error.throw(e)


def asgetparams ( **kwargs ) :
	print( lib.url.get( **kwargs ) )
