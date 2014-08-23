import os, lib.file

def concat(src, out):

	with open(out, 'w') as f:

		def callback(g):
			lib.file.read(g, f.write)
			f.write(os.linesep)

		lib.file.walk(src, callback)


def append(out, txt):

	with open(out, 'a') as f:
		f.write(txt)
		f.write(os.linesep)