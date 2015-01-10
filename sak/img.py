import os, subprocess

def x2eps(img, out = None, width = None, height = None):
	inkscape.convert(img, out, width, height, '-E', '.eps')

def x2png(img, out = None, width = None, height = None):
	inkscape.convert(img, out, width, height, '-e', '.png')

def x2pdf(img, out = None, width = None, height = None):
	inkscape.convert(img, out, width, height, '-A', '.pdf')

def x2svg(img, out = None, width = None, height = None):
	inkscape.convert(img, out, width, height, '-l', '.svg')

def resize(img, out, width, height, mode = '^'):
	subprocess.call(['convert', img, '-resize', '%sx%s%s' % (width, height, mode), out])

def crop(img, out, width, height, gravity = 'Center', left = '0', top = '0'):
	subprocess.call(['convert', img, '-gravity', gravity, '-crop', '%sx%s+%s+%s' % (width, height, left, top), out])


class inkscape(object):
	def convert(img, out, width, height, t, ext):

		if out is None:
			base, _ = os.path.splitext(img)
			out = base + ext

		args = ['inkscape', '-z', '-T', t, out, img]

		if width  is not None : args.extend(['--export-width' , width ])
		if height is not None : args.extend(['--export-height', height])

		subprocess.call(['inkscape', '-z', '-T', t, out, img])
