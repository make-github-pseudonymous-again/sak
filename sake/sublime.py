import os, json, lib.json

def projectjson(path):
	return {
		'folders' : [
			{
				'path' : path,
				'folder_exclude_patterns': []
			}
		]
	}

def projectpath(directory):
	root = os.path.abspath(directory)
	name = os.path.basename(root)
	return root, os.path.join(root, name + '.sublime-project')

def workspacepath(directory):
	root = os.path.abspath(directory)
	name = os.path.basename(root)
	return root, os.path.join(root, name + '.sublime-workspace')

def configdir(v):
	return os.path.expanduser('~/.config/sublime-text-') + str(v)

def configdirs():
	for v in [2, 3] :
		d = configdir(v)
		if os.path.isdir(d): yield d

def sessionfile(d):
	return os.path.join(d, "Settings", "Session.sublime_session")


def add(directory = '.', *others):
	path, fproject = projectpath(directory)

	with open(fproject, 'w') as f:
		project = projectjson(path)
		json.dump(project, f, indent = '\t')

	for d in configdirs():

		fsession = sessionfile(d)

		with lib.json.proxy(fsession, "w", strict = False, indent = '\t', throws = True) as config :
			config['workspaces']['recent_workspaces'].insert(0, fproject)

	if others : add(*others)

def remove(directory = '.', *others):
	path, fproject = projectpath(directory)

	if os.path.isfile(fproject) : os.remove(fproject)
	else : print("could not find '%s'" % fproject)

	path, fworkspace = workspacepath(directory)
	if os.path.isfile(fworkspace) : os.remove(fworkspace)

	for d in configdirs():

		fsession = sessionfile(d)

		with lib.json.proxy(fsession, "w", strict = False, indent = '\t', throws = True) as config :
			recent = config['workspaces']['recent_workspaces']
			if fproject in recent : recent.remove(fproject)

	if others : remove(*others)
