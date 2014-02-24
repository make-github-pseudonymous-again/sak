import os, json


def mk(directory = '.'):
	full = os.path.abspath(directory)
	path = full + '/' + os.path.basename(full) + '.sublime-project'
	with open(path, 'w') as f:
		project = {'folders' : [{ 'path' : os.path.abspath(directory), 'folder_exclude_patterns': [] }]}
		json.dump(project, f, indent = '\t')

	for i in [2, 3]:

		d = os.path.expanduser('~/.config/sublime-text-') + str(i)

		if os.path.isdir(d):

			with open(d + '/Settings/Session.sublime_session', 'r') as f:
				config = json.load(f, strict = False)

			config['workspaces']['recent_workspaces'].insert(0, path)

			with open(d + '/Settings/Session.sublime_session', 'w') as f:
				json.dump(config, f, indent = '\t')

def rm(directory = '.'):
	full = os.path.abspath(directory)
	path = full + '/' + os.path.basename(full) + '.sublime-project'
	os.remove(path)

	workspace_path = full + '/' + os.path.basename(full) + '.sublime-workspace'
	if os.path.isfile(workspace_path) : os.remove(workspace_path)

	for i in [2, 3]:

		d = os.path.expanduser('~/.config/sublime-text-') + str(i)

		if os.path.isdir(d):

			with open(d + '/Settings/Session.sublime_session', 'r') as f:
				config = json.load(f, strict = False)

			config['workspaces']['recent_workspaces'].remove(path)

			with open(d + '/Settings/Session.sublime_session', 'w') as f:
				json.dump(config, f, indent = '\t')