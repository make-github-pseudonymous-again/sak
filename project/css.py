import lib.color, lib.css

def hex2rgba(h):
	print(lib.css.rgba2str(*lib.color.hex2rgb(h)))

def hex2rgb(h):
	print(lib.css.rgb2str(*lib.color.hex2rgb(h)[:-1]))

def rgb2hex(rgb):
	print(lib.color.rgb2hex(*lib.css.str2rgb(rgb)))

def rgba2hex(rgb):
	print(lib.color.rgba2hex(*lib.css.str2rgb(rgb)))

def darken(inp, p):
	if inp[0] == 'r' : print(lib.css.rgb2str(*lib.color.darken(*lib.css.str2rgb(inp), p = int(p))))
	else             : print(lib.color.rgb2hex(*lib.color.darken(*lib.color.hex2rgb(inp)[:-1], p = int(p))))

def lighten(inp, p):
	if inp[0] == 'r' : print(lib.css.rgb2str(*lib.color.lighten(*lib.css.str2rgb(inp), p = int(p))))
	else             : print(lib.color.rgb2hex(*lib.color.lighten(*lib.color.hex2rgb(inp)[:-1], p = int(p))))


def rgb2hsl(rgb):
	print(lib.css.hsl2str(*lib.color.rgb2hsl(*lib.css.str2rgb(rgb))))

def rgba2hsla(rgb):
	print(lib.css.hsla2str(*lib.color.rgba2hsla(*lib.css.str2rgb(rgb))))
