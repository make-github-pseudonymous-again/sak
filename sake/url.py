import lxml.html


def href(url):
	tree = lxml.html.parse(url)
	title = tree.find('.//title').text
	fmt = '<a href="%s">%s</a>'
	print(fmt % (url, title))