
import subprocess, collections, lib.file, lib.error, lib.check

def npm(*args):
	subprocess.call(['npm'] + list(args))

def publish():
	npm('publish')

def build():
	npm('run', 'build')

def doc():
	npm('run', 'doc')

def test():
	npm('test')

def clean():
	lib.file.rm('node_modules', 'coverage', 'doc', recursive = True, force = True)


try:

	import semantic_version
	import os, lib.json, lib.git, lib.list, lib.ver


	NPM   = 'package.json'
	BOWER = 'bower.json'

	PM = [NPM, BOWER]

	VERSION_HASH   = 'version'


	def release(version, message = None):
		doc()
		version = setversion(version)
		push(version, message)

	def setversion(version):
		special = version in lib.ver.KEYS
		check   = not special
			
		if check :
			lib.check.SemverVersionTagNotValidException(version)
			v = semantic_version.Version(version)

		olds = []

		for pm in PM:
			if os.path.isfile(pm):
				with lib.json.proxy(pm, 'r') as conf:
					if VERSION_HASH in conf:
						old = conf[VERSION_HASH]
						lib.check.OldSemverVersionTagNotValidException(old, pm)
						if check :
							lib.check.NewSemverVersionTagNotGreaterException(version, old)

						olds.append(old)


		if special and len(olds) == 0 :
			print("cannot infer version number from '%s' without at least a package configuration file" % version)
			return

		if not lib.list.one(olds) :
			print("versions MUST be equal in packages configuration files %s" % list(zip(PM, olds)))
			return

		if special :
			version = lib.ver.resolve(olds[0], version)

		for pm in PM:
			if os.path.isfile(pm):
				with lib.json.proxy(pm, 'w', object_pairs_hook = collections.OrderedDict) as conf:
					conf[VERSION_HASH] = version

		return version

	def push(version, message = None):
		version = lib.ver.PREFIX + version
		if message is None : message = version

		build()
		lib.git.add('--all', '.')
		lib.git.commit('-am', message)
		lib.git.push()
		lib.git.tag('-a', version, '-m', message)
		lib.git.push('--tags')
		publish()


except ImportError as cause:

	e = lib.error.ModuleMissingException(cause, "semantic_version")

	release = lambda version, message = None : lib.error.throw(e)

	setversion = lambda version : lib.error.throw(e)

	push = lambda version, message = None : lib.error.throw(e)

