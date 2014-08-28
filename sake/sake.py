from __future__ import absolute_import, division, print_function, unicode_literals

import os, lib.git

def git(action, *args):
	path = os.path.join(__file__, '..', '..')
	path = os.path.abspath(path)
	lib.git.do(action, *args, cwd = path)

def pull(*args):
	git('pull', *args)

def push(*args):
	git('push', *args)

def commit(*args):
	git('commit', *args)

def add(*args):
	git('add', *args)

def status(*args):
	git('status', *args)

def diff(*args):
	git('diff', *args)
