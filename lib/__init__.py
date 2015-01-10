
__all__ = []

def __init__():
	import os
	root = os.path.dirname(os.path.abspath(__file__))
	module = os.path.basename(root)

	for f in os.listdir(root):
		path = root + '/' + f
		if os.path.isdir(path):
			if os.path.isfile(path + '/__init__.py'):
				__import__(module + '.' + f)
				__all__.append(f)

		if os.path.isfile(path) and f != '__init__.py':
			name, ext = os.path.splitext(f)

			if ext == '.py':
				__import__(module + '.' + name)
				__all__.append(name)



__init__()
