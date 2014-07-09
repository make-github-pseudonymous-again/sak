
import subprocess

def publish():
	subprocess.call(['npm', 'publish'])

def build():
	subprocess.call(['npm', 'run', 'build'])

def test():
	subprocess.call(['npm', 'test'])	


try:

	import semantic_version
	import os, lib.json, lib.git, lib.list


	NPM   = 'package.json'
	BOWER = 'bower.json'

	PM = [NPM, BOWER]

	VERSION_PREFIX = 'v'
	VERSION_HASH   = 'version'

	SPECIAL  = ['major', 'minor', 'patch']


	def release(version, message = None):

		special = version in SPECIAL
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
			v = semantic_version.Version(olds[0])
			setattr(v, version, getattr(v, version) + 1)
			version = str(v)



		for pm in PM:
			if os.path.isfile(pm):
				with lib.json.proxy(pm, 'w') as conf:
					conf[VERSION_HASH] = version


		version = VERSION_PREFIX + version
		if message is None : message = version

		build()
		lib.git.add('--all', '.')
		lib.git.commit('-am', message)
		lib.git.push()
		lib.git.tag('-a', version, '-m', message)
		lib.git.push('--tags')
		publish()


except ImportError as e:

	_e = e

	def release():
		print(_e, ': to fix this --> pip3 install semantic_version')

