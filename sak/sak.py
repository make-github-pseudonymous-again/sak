import os , sak , lib.git , lib.sak

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


def main ( inp ) :

	"""
		>>> from sak.sak import *
		>>> main( [ 'ts' , 'd' , 'a' , '2' ] )
		2 10

	"""

	hierarchy , action , inp = lib.sak.findaction( sak , inp , ['sak'] )
	args , kwargs = lib.sak.assignarguments( hierarchy , action , inp )
	action( *args , **kwargs )
