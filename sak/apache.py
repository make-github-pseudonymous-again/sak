import os, os.path

def install(source = ".", name = None, www = "/var/www"):
	source = os.path.abspath(source)
	if name is None : name = os.path.basename(source)
	link_name = os.path.join(www, name)
	os.symlink(source, link_name)

def uninstall(name = None, www = "/var/www"):
	if name is None : name = os.path.basename(".")
	link_name = os.path.join(www, name)
	os.remove(link_name)
