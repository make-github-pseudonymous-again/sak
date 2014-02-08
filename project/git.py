"""
	git module

	some git snippets freely derived from https://github.com/badele/gitcheck
"""


import os, subprocess, re, functools, lib.ansy


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
	return do(update.__name__, *args)


def pull(*args):
	return do(pull.__name__, *args)


def push(*args):
	return do(push.__name__, *args)



class helper:

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


	def recursive(args, callback):
		if len(args) == 0 : args = ['.']

		for d in args:
			l = [x for x in os.listdir(d) if os.path.isdir(os.path.join(d, x))]
			if len(l) == 0 : continue
			if '.git' in l : callback(d)
			else           : helper.recursive([os.path.join(d, x) for x in l], callback)


	def call(*args, **kwargs):
		return functools.partial(
			subprocess.Popen,
			stdin = subprocess.PIPE,
			stdout = subprocess.PIPE,
			stderr = subprocess.PIPE
		)(*args, **kwargs).communicate()


	BRANCH = re.compile(r'^\* (.*)')

	def branch(d):
		out, _ = helper.call(['git', 'branch'], cwd = d)
		m = helper.BRANCH.match(out.decode())
		return None if m is None else m.group(1)

	def remotes(d):
		out, _ = helper.call(['git', 'remote'], cwd = d)
		return out.decode().split('\n')[:-1]

	def update(d):
		helper.call(['git', 'remote', 'update'], cwd = d)

	def push(d):
		helper.call(['git', 'push'], cwd = d)

	def pull(d):
		helper.call(['git', 'pull'], cwd = d)

	def pulls(d, remote, branch):
		return helper.commits(d, 'HEAD', '%s/%s' % (remote, branch))

	def pushs(d, remote, branch):
		return helper.commits(d, '%s/%s' % (remote, branch), 'HEAD')

	def commits(d, a, b):
		out, _ = helper.call(['git', 'log', '%s..%s' % (a, b),  '--oneline'], cwd = d)
		return out.decode().split('\n')[:-1]

	def locals(d):
		out, _ = helper.call(['git', 'status', '--porcelain', '-u'], cwd = d)
		return [c for c in out.decode().split('\n')[:-1]]

	def hasbranch(d, remote, branch):
		out, _ = helper.call(['git', 'branch', '-r'], cwd = d)
		return out.decode().find('%s/%s' % (remote, branch)) != -1


	def pretty(d, lo, fr, to):
		r = [] if len(lo) == 0 else ['local[%d]' % len(lo)]
		for key in fr :
			if len(fr[key]) > 0 or len(to[key]) > 0:
				r.append('%s[pull:%d, push:%d]' % (key, len(fr[key]), len(to[key])))

		if len(r) > 0 : print(' '.join([d] + r))