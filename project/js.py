import os, lib.file

def build(root, ugly = '-uno', src = 'src', out = 'min'):

	data = os.path.join(root, src)
	for l in os.listdir(data):

		curr = os.path.join(data, l)
		if not os.path.isdir(curr) : continue

		path = os.path.join(root, out, '%s.js' % l)

		with open(path, 'w') as f:

			def callback(g):
				lib.file.read(g, f.write)
				f.write(os.linesep)

			lib.file.walk(curr, callback)

		if ugly != '-uno' : uglify(path)


def uglify(path,  dest = None):
	if dest is None : dest = path
	os.system('uglifyjs ' + path + ' -o ' + dest + ' -m -c')
