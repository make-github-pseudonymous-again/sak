import os, lib.file, lib.git, lib.tex

def build(src, out):


	def add(path, f):

		def callback(g):
			lib.file.read(g, f.write)
			f.write(os.linesep)

		if os.path.isdir(path) : lib.file.walk(path, callback)

		elif os.path.isfile('%s.tex' % path):
			with open('%s.tex' % path) as g : callback(g)


	with open(out, 'w') as f:
		a = lambda x : add(os.path.join(src, x), f)
		w = f.write
		a('preamble')
		w('\\begin{document}\n')
		a('title')
		a('before')
		a('main')
		w('\\appendix\n')
		a('appendix')
		a('after')
		w('\\end{document}\n')



def ignore(name):
	for item in lib.tex.out(name):
		print(item)

def clean(name):
	files = lib.tex.out(name)
	lib.file.rm(files)
