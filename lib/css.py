


def parsergb(rgb):
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

def reprrgb(r, g, b):
	return 'rgb(%d, %d, %d)' % (r, g, b)

def reprrgba(r, g, b, a):
	return 'rgba(%d, %d, %d, %.2f)' % (r, g, b, a / 255)