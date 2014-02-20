


def rgba2hex(r, g, b, a = None):
	if a is None : return rgb2hex(r, g, b)
	return '#%02x%02x%02x%02x' % (r, g, b, a)

def rgb2hex(r, g, b):
	return '#%02x%02x%02x' % (r, g, b)

def parsehex(h):
	if len(h) < 9 : h += 'ff'
	return [int(h[i:i+2], 16) for i in range(1, 9, 2)]

def darken(r, g, b, p):
	return lighten(r, g, b, -p)

def lighten(r, g, b, p):
	return map(lambda x : int(min(255, x + (p / 100) * (255 - x))), [r,g,b])