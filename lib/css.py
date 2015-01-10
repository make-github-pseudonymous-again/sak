
def rgba2hex(r, g, b, a = None):
	if a is None : return rgb2hex(r, g, b)
	return '#%02x%02x%02x%02x' % tuple(map(round, [r, g, b, a]))

def rgb2hex(r, g, b):
	return '#%02x%02x%02x' % tuple(map(round, [r, g, b]))

def hex2rgb(h):
	if len(h) < 9 : h += 'ff'
	return [int(h[i:i+2], 16) for i in range(1, 9, 2)]



def str2rgb(rgb):
	if rgb[3] == 'a':
		x = rgb[5:-1].split(',')
		r, g, b = map(int, x[:-1])
		a = int(255 * float(x[-1]))
		return [r, g, b, a]

	else:
		r, g, b = map(int, rgb[4:-1].split(','))
		return [r, g, b]


def rgb2str(r, g, b):
	return 'rgb(%d, %d, %d)' % tuple(map(round, [r, g, b]))

def rgba2str(r, g, b, a):
	return 'rgba(%d, %d, %d, %.2f)' % tuple(map(round, [r, g, b, a / 255]))

def str2hsl(hsl):
	if hsl[3] == 'a':
		x = hsl[5:-1].split(',')
		h = int(x[0])
		s = int(x[1][:-1]) / 100
		l = int(x[2][:-1]) / 100 * 255
		a = int(255 * float(x[-1]))
		return [h, s, l, a]
	else:
		x = hsl[4:-1].split(',')
		h = int(x[0])
		s = int(x[1][:-1]) / 100
		l = int(x[2][:-1]) / 100 * 255
		return [h, s, l]


def hsl2str(h, s, l):
	return 'hsl(%d, %d%%, %d%%)' % (h, round(s * 100), round(l / 255 * 100))

def hsla2str(h, s, l, a):
	return 'hsla(%d, %d%%, %d%%, %.2f)' % (h, round(s * 100), round(l / 255 * 100), a / 255)
