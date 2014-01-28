#!/usr/bin/python3

import sys, project


def main(arg):
	if len(arg) < 2 : return

	submodule = getattr(project, arg[0])
	action = getattr(submodule, arg[1])
	action(*arg[2:])

if __name__ == '__main__':
	main(sys.argv[1:])
