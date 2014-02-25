import os, subprocess

def svg2eps(img, out = None):
	helper.do(img, out, '-E', '.eps')

def svg2png(img, out = None):
	helper.do(img, out, '-e', '.png')

def svg2pdf(img, out = None):
	helper.do(img, out, '-A', '.pdf')

def eps2svg(img, out = None):
	helper.do(img, out, '-l', '.svg')


class helper:
	def do(img, out, t, ext):

		if out is None:
			base, _ = os.path.splitext(img)
			out = base + ext

		subprocess.call(['inkscape', '-z', '-T', t, out, img])