import os, lib.file, subprocess

__JSEXT__ = '%s.js'
__INTRO__ = __JSEXT__ % 'intro'
__OUTRO__ = __JSEXT__ % 'outro'
__INDEX__ = __JSEXT__ % 'index'

def build(root, ugly = '-uno', src = 'src', out = 'min'):

	result = os.path.join(root, out);

	if not os.path.exists(result) : os.makedirs(result)

	data = os.path.join(root, src)
	for l in os.listdir(data):

		curr = os.path.join(data, l)
		if not os.path.isdir(curr) : continue

		path = os.path.join(result, __JSEXT__ % l)

		with open(path, 'w') as f:

			def fhandle(path):
				with open(path, 'r') as g:
					f.write(os.linesep)
					f.write('/* ' + g.name + ' */')
					f.write(os.linesep)
					f.write(os.linesep)
					lib.file.read(g, f.write)
					f.write(os.linesep)

			def dhandle(d):

				el = set(os.listdir(d))

				intro = __INTRO__ in el
				outro = __OUTRO__ in el
				index = __INDEX__ in el

				if intro : el.remove(__INTRO__)
				if outro : el.remove(__OUTRO__)
				if index : el.remove(__INDEX__)

				if intro : fhandle(__INTRO__)

				for e in sorted(el):
					path = os.path.join(d, e)

					if   os.path.isdir(path)        : dhandle(path)
					elif f and os.path.isfile(path) : fhandle(path)

				if outro : fhandle(__OUTRO__)


			dhandle(curr)

		if ugly != '-uno' : uglify(path)


def uglify(path,  dest = None):
	if dest is None : dest = path
	subprocess.call(['uglifyjs', path, '-o', dest, '-m', '-c'])
