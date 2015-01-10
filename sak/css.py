import lib.color, lib.css, subprocess

def build(src, ugly = None):
	cmd = ['compass', 'compile', src]
	if ugly is not None : cmd += ['-e', 'production', '--force']
	subprocess.call(cmd)

def watch(src):
	cmd = ['compass', 'watch', src]
	subprocess.call(cmd)

def hex2rgba(h):
	print(lib.css.rgba2str(*lib.css.hex2rgb(h)))

def hex2rgb(h):
	print(lib.css.rgb2str(*lib.css.hex2rgb(h)[0:3]))

def rgb2hex(rgb):
	print(lib.css.rgb2hex(*lib.css.str2rgb(rgb)))

def rgba2hex(rgb):
	print(lib.css.rgba2hex(*lib.css.str2rgb(rgb)))

def darken(inp, p):
	helper.light(inp, p, lib.color.darken)

def lighten(inp, p):
	helper.light(inp, p, lib.color.lighten)

def rgb2hsl(rgb):
	print(lib.css.hsl2str(*lib.color.rgb2hsl(*lib.css.str2rgb(rgb))))

def rgba2hsla(rgb):
	print(lib.css.hsla2str(*lib.color.rgba2hsla(*lib.css.str2rgb(rgb))))

def hsl2rgb(hsl):
	print(lib.css.rgb2str(*lib.color.hsl2rgb(*lib.css.str2hsl(hsl))))

def hsla2rgba(hsl):
	print(lib.css.rgba2str(*lib.color.hsla2rgba(*lib.css.str2hsl(hsl))))


class helper(object):
	def light(inp, p, transform):

		if inp[0] == 'r':
			out = lambda *x : lib.css.rgb2str(*lib.color.hsl2rgb(*x))
			hsl = lib.color.rgb2hsl(*lib.css.str2rgb(inp))
		elif inp[0] == 'h':
			out = lib.css.hsl2str
			hsl = lib.css.str2hsl(inp)
		else:
			out = lambda *x : lib.css.rgb2hex(*lib.color.hsl2rgb(*x))
			hsl = lib.color.rgb2hsl(*lib.css.hex2rgb(inp)[0:3])

		print(out(*transform(*hsl, p = int(p))))
