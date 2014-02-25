import os, subprocess

def svg2eps(img, out = None):
	helper.svg2other(img, out, '-E', '.eps')

def svg2png(img, out = None):
	helper.svg2other(img, out, '-e', '.png')

def svg2pdf(img, out = None):
	helper.svg2other(img, out, '-A', '.pdf')



class helper:
	def svg2other(img, out, t, ext):

		if out is None:
			base, ext = os.path.splitext(img)
			out = img + ext

		subprocess.call(['inkscape', '-z', '-T', t, out, img])