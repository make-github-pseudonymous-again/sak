import lib.bower

def register(bowername, gitendpoint, force = False):
	lib.bower.register(bowername, gitendpoint, force = force)

def unregister(bowername, force = False):
	lib.bower.unregister(bowername, force = force)
