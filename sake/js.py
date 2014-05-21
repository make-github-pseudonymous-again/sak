import os, lib.file

def build(root, ugly = '-uno', src = 'src', out = 'min'):

	result = os.path.join(root, out);

	if not os.path.exists(result) : os.makedirs(result)

	data = os.path.join(root, src)
	for l in os.listdir(data):

		curr = os.path.join(data, l)
		if not os.path.isdir(curr) : continue

		path = os.path.join(result, '%s.js' % l)

		with open(path, 'w') as f:

			def callback(g):
				f.write(os.linesep)
				f.write('/* ' + g.name + ' */')
				f.write(os.linesep)
				f.write(os.linesep)
				lib.file.read(g, f.write)
				f.write(os.linesep)

			lib.file.walk(curr, callback)

		if ugly != '-uno' : uglify(path)


def uglify(path,  dest = None):
	if dest is None : dest = path
	os.system('uglifyjs ' + path + ' -o ' + dest + ' -m -c')
