import lib.color, lib.css

def hex2rgba(h):
	print(lib.css.reprrgba(*lib.color.parsehex(h)))

def hex2rgb(h):
	print(lib.css.reprrgb(*lib.color.parsehex(h)[:-1]))

def rgb2hex(rgb):
	print(lib.color.rgb2hex(*lib.css.parsergb(rgb)))

def rgba2hex(rgb):
	print(lib.color.rgba2hex(*lib.css.parsergb(rgb)))

def darken(inp, p):
	if inp[0] == 'r' : print(lib.css.reprrgb(*lib.color.darken(*lib.css.parsergb(inp), p = int(p))))
	else             : print(lib.color.rgb2hex(*lib.color.darken(*lib.color.parsehex(inp)[:-1], p = int(p))))

def lighten(inp, p):
	if inp[0] == 'r' : print(lib.css.reprrgb(*lib.color.lighten(*lib.css.parsergb(inp), p = int(p))))
	else             : print(lib.color.rgb2hex(*lib.color.lighten(*lib.color.parsehex(inp)[:-1], p = int(p))))
