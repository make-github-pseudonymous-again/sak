

def rgba2hex(r, g, b, a = None):
	if a is None : return rgb2hex(r, g, b)
	return '#%02x%02x%02x%02x' % (r, g, b, a)

def rgb2hex(r, g, b):
	return '#%02x%02x%02x' % (r, g, b)

def hex2rgb(h):
	if len(h) < 9 : h += 'ff'
	return [int(h[i:i+2], 16) for i in range(1, 9, 2)]



def str2rgb(rgb):
	if rgb[3] == 'a':
		x = rgb[5:-1].split(',')
		if x[-1].isdigit():
			r, g, b, a = map(int, x)
		else:
			r, g, b = map(int, x[:-1])
			a = int(255 * float(x[-1]))
	else:
		r, g, b = map(int, rgb[4:-1].split(','))
		return r, g, b

	return r, g, b, a

def rgb2str(r, g, b):
	return 'rgb(%d, %d, %d)' % (r, g, b)

def rgba2str(r, g, b, a):
	return 'rgba(%d, %d, %d, %.2f)' % (r, g, b, a / 255)

def hsl2str(h, s, l):
	return 'hsl(%d, %d%%, %d%%)' % (h, round(s * 100), round(l / 255 * 100))

def hsla2str(h, s, l, a):
	return 'hsl(%d, %d%%, %d%%, %.2f)' % (h, round(s * 100), round(l / 255 * 100), a / 255)