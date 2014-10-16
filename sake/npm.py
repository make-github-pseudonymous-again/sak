from __future__ import absolute_import, division, print_function, unicode_literals


import subprocess, lib.file, lib.error, lib.check, lib.npm, lib.git

def npm(*args):
	return subprocess.call(['npm'] + list(args))

def publish():
	return npm('publish')

def unpublish(*args):
	return npm('unpublish', *args)

def build():
	return npm('run', 'build')

def doc():
	return npm('run', 'doc')

def test():
	return npm('test')

def install(*args):
	return npm('install', *args)

def clean():
	lib.file.rm('node_modules', 'coverage', 'doc', recursive = True, force = True)

def upload(version, message = None):
	lib.npm.upload(version, message)

try:

	import semantic_version


	def release(version, message = None):
		try :
			doc()
			build()
			version = lib.npm.setversion(version)
			lib.npm.upload(version, message)
			publish()

		finally :
			lib.git.checkout( "master" )

	def setversion(version):
		version = lib.npm.setversion(version)
		print(version)

	def getversion():
		version = lib.npm.getversion()
		print(version)


except ImportError as cause:

	e = lib.error.ModuleMissingException(cause, "semantic_version")

	release = lambda version, message = None : lib.error.throw(e)
	setversion = lambda version : lib.error.throw(e)
	getversion = lambda : lib.error.throw(e)

