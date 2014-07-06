


try:

	import semantic_version
	import os, lib.json, lib.git


	NPM   = 'package.json'
	BOWER = 'bower.json'

	PM = [NPM, BOWER]

	VERSION_PREFIX = 'v'
	VERSION_HASH   = 'version'


	def release(version, message = None):

		if not semantic_version.validate(version) :
			print("version tag '%s' not valid (http://semver.org/)" % version)
			return

		v = semantic_version.Version(version)

		for pm in PM:
			if os.path.isfile(pm):
				with lib.json.proxy(pm, 'r') as conf:
					if VERSION_HASH in conf:
						old = conf[VERSION_HASH]
						if not semantic_version.validate(old) :
							print("old version tag '%s' in '%s' not valid (http://semver.org/)" % (old, pm))
							return
						if not v > semantic_version.Version(old):
							print("version tag '%s' should be > than '%s'" % (version, old))
							return

		for pm in PM:
			if os.path.isfile(pm):
				with lib.json.proxy(pm, 'w') as conf:
					conf[VERSION_HASH] = version


		version = VERSION_PREFIX + version
		if message is None : message = version

		lib.git.add('-all', '.')
		lib.git.commit('-am', message)
		lib.git.push()
		lib.git.tag('-a', version, '-m', message)
		lib.git.push('--tags')


except ImportError as e:

	_e = e

	def release():
		print(_e, ': to fix this --> pip3 install semantic_version')

