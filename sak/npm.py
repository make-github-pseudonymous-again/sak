import subprocess, lib.file, lib.error, lib.check, lib.npm, lib.git

def npm ( *args , cwd = None ) :
	return subprocess.call(['npm'] + list(args) , cwd = cwd )

def publish( cwd = None ):
	return npm('publish', cwd = cwd)

def unpublish(*args, cwd = None ):
	return npm('unpublish', *args, cwd = cwd)

def build( cwd = None ):
	return npm('run', 'build', cwd = cwd)

def doc( cwd = None ):
	return npm('run', 'doc', cwd = cwd)

def test( cwd = None ):
	return npm('test', cwd = cwd)

def install(*args, cwd = None ):
	return npm('install', *args, cwd = cwd)

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

