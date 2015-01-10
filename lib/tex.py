

OUT = ['aux', 'idx', 'log', 'out', 'pyg', 'pdf', 'toc']

def out(name):
	for ext in OUT:
		yield '%s.%s' % (name, ext)
