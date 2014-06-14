import lxml.html


def href(url, *args):
	tree = lxml.html.parse(url)
	title = tree.find('.//title')
	if title is not None : text = title.text
	else : text = url
	fmt = '<a href="%s">%s</a>'
	print(fmt % (url, text))

	if len(args) : href(*args)