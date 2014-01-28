import os

root = os.path.dirname(__file__)

for f in os.listdir(root):
	path = root + '/' + f
	if os.path.isfile(path) and path != __file__:
		name, ext = os.path.splitext(f)
		if ext == '.py' : __import__('project.' + name)