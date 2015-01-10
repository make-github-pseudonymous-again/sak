
def darken(h, s, l, p):
	return lighten(h, s, l, -p)

def lighten(h, s, l, p):
	return h, s, l + p * 2.55

def rgb2hsl(r, g, b):
	M = max(r, g, b)
	m = min(r, g, b)
	C = M - m
	l = (M + m) / 2
	s = 0 if C == 0 else C / (255 - abs(2*l - 255))
	if   C == 0 : h = 0
	elif r == M : h = (g - b) / C
	elif g == M : h = (b - r) / C + 2
	elif b == M : h = (r - g) / C + 4
	return [round(h % 6 * 60), s , l]

def hsl2rgb(h, s, l):
	C = (255 - abs(2*l - 255)) * s
	X = C * (1 - abs((h / 60) % 2 - 1))
	if   h < 60  : r, g, b = C, X, 0
	elif h < 120 : r, g, b = X, C, 0
	elif h < 180 : r, g, b = 0, C, X
	elif h < 240 : r, g, b = 0, X, C
	elif h < 300 : r, g, b = X, 0, C
	elif h < 360 : r, g, b = C, 0, X

	m = l - C/2
	return [r + m, g + m, b + m]

def hsla2rgba(h, s, l, a):
	return hsl2rgb(h, s, l) + [a]

def rgba2hsla(r, g, b, a):
	return rgb2hsl(r, g, b) + [a]

