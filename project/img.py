import os, subprocess

def x2eps(img, out = None, width = None, height = None):
	inkscape.convert(img, out, width, height, '-E', '.eps')

def x2png(img, out = None, width = None, height = None):
	inkscape.convert(img, out, width, height, '-e', '.png')

def x2pdf(img, out = None, width = None, height = None):
	inkscape.convert(img, out, width, height, '-A', '.pdf')

def x2svg(img, out = None, width = None, height = None):
	inkscape.convert(img, out, width, height, '-l', '.svg')

def resize(img, out, width, height):
	subprocess.call(['convert', img, '-resize', '%sx%s' % (width, height), out])


class inkscape:
	def convert(img, out, width, height, t, ext):

		if out is None:
			base, _ = os.path.splitext(img)
			out = base + ext

		args = ['inkscape', '-z', '-T', t, out, img]

		if width  is not None : args.extend(['--export-width' , width ])
		if height is not None : args.extend(['--export-height', height])

		subprocess.call(['inkscape', '-z', '-T', t, out, img])