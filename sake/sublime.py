from __future__ import absolute_import, division, print_function, unicode_literals

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
	return os.path.join(root, name + '.sublime-project')

def workspacepath(directory):
	root = os.path.abspath(directory)
	name = os.path.basename(root)
	return os.path.join(root, name + '.sublime-workspace')

def configdir(v):
	return os.path.expanduser('~/.config/sublime-text-') + str(v)

def configdirs():
	for v in [2, 3] : 
		d = configdir(v)
		if os.path.isdir(d): yield d

def sessionfile(d):
	return os.path.join(d, "Settings", "Session.sublime_session")


def add(directory = '.'):
	path = projectpath(directory)

	with open(path, 'w') as f:
		project = projectjson(path)
		json.dump(project, f, indent = '\t')

	for d in configdirs():

		fsession = sessionfile(d)

		with lib.json.proxy(fsession, "w", strict = False, indent = '\t', throws = True) as config :
			config['workspaces']['recent_workspaces'].insert(0, path)

def remove(directory = '.'):
	path = projectpath(directory)

	if os.path.isfile(path) : os.remove(path)
	else : print("could not find '%s'" % path)

	workspace_path = workspacepath(directory)
	if os.path.isfile(workspace_path) : os.remove(workspace_path)

	for d in configdirs():

		fsession = sessionfile(d)

		with lib.json.proxy(fsession, "w", strict = False, indent = '\t', throws = True) as config :
			config['workspaces']['recent_workspaces'].remove(path)