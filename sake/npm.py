
import subprocess, collections, lib.file

def publish():
	subprocess.call(['npm', 'publish'])

def build():
	subprocess.call(['npm', 'run', 'build'])

def doc():
	subprocess.call(['npm', 'run', 'doc'])

def test():
	subprocess.call(['npm', 'test'])

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
		version = setversion(version)
		push(version, message)

	def setversion(version):
		special = version in lib.ver.KEYS
		check   = not special
			
		if check and not semantic_version.validate(version) :
			print("version tag '%s' not valid (http://semver.org/)" % version)
			return

		if check : v = semantic_version.Version(version)

		olds = []

		for pm in PM:
			if os.path.isfile(pm):
				with lib.json.proxy(pm, 'r') as conf:
					if VERSION_HASH in conf:
						old = conf[VERSION_HASH]
						if not semantic_version.validate(old) :
							print("old version tag '%s' in '%s' not valid (http://semver.org/)" % (old, pm))
							return
						if check and not v > semantic_version.Version(old):
							print("version tag '%s' should be > than '%s'" % (version, old))
							return

						olds.append(old)


		if special and len(olds) == 0:
			print("cannot infer version number from '%s' without at least a package configuration file" % version)
			return

		if not lib.list.one(olds) :
			print("versions MUST be equal in packages configuration files %s" % list(zip(PM, olds)))
			return

		if special:
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
		doc()
		lib.git.add('--all', '.')
		lib.git.commit('-am', message)
		lib.git.push()
		lib.git.tag('-a', version, '-m', message)
		lib.git.push('--tags')
		publish()


except ImportError as e:

	_e = e

	def release(version, message = None):
		print(_e, ': to fix this --> pip3 install semantic_version')

	def setversion(version):
		print(_e, ': to fix this --> pip3 install semantic_version')

	def push(version, message = None):
		print(_e, ': to fix this --> pip3 install semantic_version')

