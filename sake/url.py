import lib.error

try:

	import lxml.etree, urllib.request

	def href(url, *args):
		conn = urllib.request.urlopen(url)
		parser = lxml.etree.HTMLParser(encoding = "utf-8")
		tree = lxml.etree.parse(conn, parser=parser)
		title = tree.find('.//title')
		if title is not None : text = title.text
		else : text = url
		fmt = '<a href="%s">%s</a>'
		print(fmt % (url, text))

		if len(args) : href(*args)

except ImportError as cause:

	e = lib.error.ModuleMissingException(cause, "lxml")

	href = lambda url, *args : lib.error.throw(e)