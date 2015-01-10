
import lib.json, os.path, lib.fn, lib.github, lib.bitbucket, sak.github, sak.bitbucket



VENDORS = {
	lib.github.DOMAIN : sak.github,
	lib.bitbucket.DOMAIN : sak.bitbucket
}


DEPENDENCIES = ['dep', 'dep-dev']

SAVE = {
	'--save' : DEPENDENCIES[0],
	'--save-dev' : DEPENDENCIES[1]
}

FILENAME_PACKAGE_CONFIGURATION = 'package.json'

DEP = 'dep'


class package(lib.json.proxy):

	def __init__(self, mode = 'r'):
		super().__init__(FILENAME_PACKAGE_CONFIGURATION, mode)



def configOK():
	return os.path.exists(FILENAME_PACKAGE_CONFIGURATION)

def structure():
	if not os.path.exists(DEP):
		os.mkdir(DEP)

	elif not os.path.isdir(DEP):
		print('error -> dep exists and is not a directory')



def depforeach(action, pred, *args, **kwargs):

	with lib.cpm.package() as p:
		for dep in DEPENDENCIES:
			for name, package in p[dep].items():
				path = os.path.join(DEP, name)
				if pred(path):

					_args = []
					_kwargs = {}

					for val in args:
						_args.append(lib.fn.val(val, package))

					for key, val in kwargs:
						_kwargs[key] = lib.fn.val(val, package)


					action(package, *args, **kwargs)
