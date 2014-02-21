


def darken(r, g, b, p):
	return lighten(r, g, b, -p)

def lighten(r, g, b, p):
	return map(lambda x : round(min(255, x + (p / 100) * 255)), [r,g,b])

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
	return round(h%6 * 60), s , l

def rgba2hsla(r, g, b, a):
	return rgb2hsl(r, g, b) + (a,)
	