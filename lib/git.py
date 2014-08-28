from __future__ import absolute_import, division, print_function, unicode_literals

import os, lib.sys

IGNORE = '.gitignore'

def do(action, *args, **kwargs):
	lib.sys.call(['git', action] + list(args), stddefault = None, **kwargs)

def clone(*args, **kwargs):
	do('clone', *args, **kwargs)

def pull(*args, **kwargs):
	do('pull', *args, **kwargs)

def push(*args, **kwargs):
	do('push', *args, **kwargs)

def commit(*args, **kwargs):
	do('commit', *args, **kwargs)

def add(*args, **kwargs):
	do('add', *args, **kwargs)

def status(*args, **kwargs):
	do('status', *args, **kwargs)

def diff(*args, **kwargs):
	do('diff', *args, **kwargs)

def tag(*args, **kwargs):
	do('tag', *args, **kwargs)

def log(*args, **kwargs):
	do('log', *args, **kwargs)