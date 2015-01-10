import lib.cpm, lib.config, lib.git, lib.http, os.path


def update():
	pred = lambda x : os.path.exists(x)
	lib.cpm.depforeach(lib.git.pull, pred, cwd = lambda p : os.path.join(lib.cpm.DEP + p))


def install(package = None, mode = None):

	lib.cpm.structure()

	if package is None:
		pred = lambda x : not os.path.exists(x)
		lib.cpm.depforeach(lib.git.clone, pred, cwd = lib.cpm.DEP)

	else:

		url = lib.repo.resolve(package, lib.cpm.VENDORS)

		if url is None:
			print('unable to find repo')
			return

		lib.git.clone(url, cwd = lib.cpm.DEP)

		if mode in SAVE:
			which = SAVE[mode]
			parts = os.path.split(p.path)
			name, _ = os.path.splitext(parts)
			with lib.cpm.package('w') as p:
				p[which][name] = url


def init():
	if not lib.cpm.configOK():
		with lib.cpm.package('w') as p:
			p['name'] = ''
			p['dep'] = {}
			p['dep-dev'] = {}
			p['version'] = '0.0.0'
			p['keywords'] = {}
			p['run'] = {}
			p['bugs'] = {}
			p['bugs']['url'] = ''
			p['author'] = ''
			p['description'] = ''
			p['repo'] = {}
			p['repo']['url'] = ''
			p['repo']['type'] = ''
			p['home'] = ''
			p['license'] = ''

	lib.cpm.structure()
