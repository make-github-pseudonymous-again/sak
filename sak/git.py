"""
	git module

	some git snippets freely derived from https://github.com/badele/gitcheck
"""


import os, subprocess, re, functools, lib.sys


def info(*args):

	def callback(d):
		lo = helper.locals(d)
		fr = {}
		to = {}

		branch = helper.branch(d)

		for remote in helper.remotes(d):
			if helper.hasbranch(d, remote, branch):
				fr[remote] = helper.pulls(d, remote, branch)
				to[remote] = helper.pushs(d, remote, branch)

		helper.pretty(d, lo, fr, to)

	return helper.wrap(args, callback)


def do(action, *args):

	def callback(d):
		print('%s \'%s\'' % (action, d))
		getattr(helper, action)(d)

	return helper.wrap(args, callback)

def update(*args):
	return do('update', *args)

def up(*args):
	return do('up', *args)

def pull(*args):
	return do('pull', *args)


def commit(*cmplxargs):

	args, dirs = helper.parsecmplx(*cmplxargs)

	def callback(d):
		print('%s \'%s\'' % ("commit", d))
		helper.commit(d, *args)

	return helper.wrap(dirs, callback)

def add(*cmplxargs):

	args, dirs = helper.parsecmplx(*cmplxargs)

	def callback(d):
		print('%s \'%s\'' % ("add", d))
		helper.add(d, *args)

	return helper.wrap(dirs, callback)


def push(*args):
	return do('push', *args)

def ls(*args):
	return do('ls', *args)

def count(*args):

	n = [0]

	def callback(d):
		n[0] += 1

	helper.wrap(args, callback)

	print(n[0])





class helper(object):

	class exception(Exception):
		def __init__(self, what):
			Exception.__init__(self, what)

		def what(self):
			return self.args[0]

		def __repr__(self):
			return self.what()

	def check(args):
		for d in args:
			if not os.path.isdir(d):
				raise helper.exception('[Errno 2] No such file or directory: \'%s\'' % d)

	def wrap(args, callback):

		try:
			helper.check(args)
			helper.recursive(args, callback)

		except helper.exception as e:
			print(e)

	def parsecmplx(*cmplxargs):

		try :
			i = list(cmplxargs).index("--")
		except Exception as e:
			i = len(cmplxargs)

		return cmplxargs[:i], cmplxargs[i+1:]


	def recursive(args, callback):
		if len(args) == 0 : args = ['.']

		for d in args:
			l = [x for x in os.listdir(d) if os.path.isdir(os.path.join(d, x))]
			if len(l) == 0 : continue
			if '.git' in l : callback(d)
			else           : helper.recursive([os.path.join(d, x) for x in l], callback)


	BRANCH = re.compile(r'^\* (.*)')

	def branch(d):
		out, _, _ = lib.sys.call(['git', 'branch'], cwd = d)
		m = helper.BRANCH.match(out.decode())
		return None if m is None else m.group(1)

	def remotes(d):
		out, _, _ = lib.sys.call(['git', 'remote'], cwd = d)
		return out.decode().split('\n')[:-1]

	def update(d):
		subprocess.call(['git', 'remote', 'update'], cwd = d)

	def up(d):
		subprocess.call(['git', 'up'], cwd = d)

	def commit(d, *args):
		subprocess.call(['git', 'commit'] + list(args), cwd = d)

	def add(d, *args):
		subprocess.call(['git', 'add'] + list(args), cwd = d)

	def push(d):
		subprocess.call(['git', 'push'], cwd = d)

	def pull(d):
		subprocess.call(['git', 'pull'], cwd = d)

	def ls(d):
		pass

	def pulls(d, remote, branch):
		return helper.commits(d, 'HEAD', '%s/%s' % (remote, branch))

	def pushs(d, remote, branch):
		return helper.commits(d, '%s/%s' % (remote, branch), 'HEAD')

	def commits(d, a, b):
		out, _, _ = lib.sys.call(['git', 'log', '%s..%s' % (a, b),  '--oneline'], cwd = d)
		return out.decode().split('\n')[:-1]

	def locals(d):
		out, _, _ = lib.sys.call(['git', 'status', '--porcelain', '-u'], cwd = d)
		return [c for c in out.decode().split('\n')[:-1]]

	def hasbranch(d, remote, branch):
		out, _, _ = lib.sys.call(['git', 'branch', '-r'], cwd = d)
		return out.decode().find('%s/%s' % (remote, branch)) != -1


	def pretty(d, lo, fr, to):
		r = [] if len(lo) == 0 else ['local[%d]' % len(lo)]
		for key in fr :
			if len(fr[key]) > 0 or len(to[key]) > 0:
				r.append('%s[pull:%d, push:%d]' % (key, len(fr[key]), len(to[key])))

		if len(r) > 0 : print(' '.join([d] + r))
