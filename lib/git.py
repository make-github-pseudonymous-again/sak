
import lib.sys

IGNORE = '.gitignore'

def do(action, *args, **kwargs):
	return lib.sys.call(['git', action] + list(args), stddefault = None, **kwargs)

def clone(*args, **kwargs):
	return do('clone', *args, **kwargs)

def pull(*args, **kwargs):
	return do('pull', *args, **kwargs)

def push(*args, **kwargs):
	return do('push', *args, **kwargs)

def commit(*args, **kwargs):
	return do('commit', *args, **kwargs)

def remote(*args, **kwargs):
	return do('remote', *args, **kwargs)

def add(*args, **kwargs):
	return do('add', *args, **kwargs)

def status(*args, **kwargs):
	return do('status', *args, **kwargs)

def diff(*args, **kwargs):
	return do('diff', *args, **kwargs)

def tag(*args, **kwargs):
	return do('tag', *args, **kwargs)

def log(*args, **kwargs):
	return do('log', *args, **kwargs)

def checkout(*args, **kwargs):
	return do('checkout', *args, **kwargs)

def submodule(*args, **kwargs):
	return do('submodule', *args, **kwargs)
