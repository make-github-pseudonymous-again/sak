

def image ( title, img ) :
	return "![%s](%s)" % ( title, img )


def link ( text, href ) :
	return "[%s](%s)" % ( text, href )


def imagewithlink ( title, img, href ) :
	text = image( title, img )
	return link( text, href )
