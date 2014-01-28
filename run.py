#!/usr/bin/python3

import os, sys, json


def sublime_mk_project(directory):
	full = os.path.abspath(directory)
	path = full + '/' + os.path.basename(full) + '.sublime-project'
	with open(path, 'w') as f:
		f.write(
'''{{
	"folders":
	[
		{{
			"path": "{0}"
		}}
	]
}}'''.format(os.path.abspath(directory)))

	for i in [2, 3]:

		d = os.path.expanduser('~/.config/sublime-text-') + str(i)

		if os.path.isdir(d):

			with open(d + '/Settings/Session.sublime_session', 'r') as f:
				config = json.load(f, strict = False)

			config['workspaces']['recent_workspaces'].insert(0, path)

			with open(d + '/Settings/Session.sublime_session', 'w') as f:
				json.dump(config, f, indent = '\t')

def sublime_rm_project(directory):
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


def main(arg):
	if len(arg) < 2 : return

	if arg[0] == 'sublime':
		if arg[1] == 'mk' and len(arg) > 2 : sublime_mk_project(arg[2])
		elif arg[1] == 'rm' and len(arg) > 2 : sublime_rm_project(arg[2])


if __name__ == '__main__':
	main(sys.argv[1:])
