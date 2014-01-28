#!/usr/bin/python3

import os, sys, json


def sublime_create_project(directory):
	path = os.path.abspath(directory + '/' + directory + '.sublime-project')
	with open(path, 'r') as f:
		f.write(
'''{
	"folders":
	[
		{
			"path": "%s"
		}
	]
}'''.format(os.path.abspath(directory)))

	for i in [2, 3]:
		d = os.path.expanduser('~/.config/sublime-text-') + str(i)
		if(os.path.isdir(d)):
			with open(d + '/Settings/Session.sublime_session', 'rw') as f:
				config = json.load(f, strict=False)
				config['workspaces']['recent_workspaces'].insert(0, path)
				json.dump(config, f, indent='\t')



def main(arg):
	if(arg[0] == 'sublime'):
		if(arg[1] == 'create'):
			sublime_create_project(arg[2])


if __name__ == '__main__':
	main(sys.argv)
