import lib.cpm, sake.github, sake.bitbucket, urllib.parse, lib.config, lib.git, lib.http, os.path

VENDORS = {
	sake.github.DOMAIN : sake.github,
	sake.bitbucket.DOMAIN : sake.bitbucket
}

DEPENDENCIES = ['dep', 'dev']

SAVE = {
	'--save' : DEPENDENCIES[0],
	'--save-dev' : DEPENDENCIES[1]
}

LIB = 'lib'

def install(package = None, save = None):

	lib.cpm.libENSURE()

	if package is None:
		with lib.cpm.package() as p:
			for dep in DEPENDENCIES:
				for name, package in p[dep].items():
					path = os.path.join(LIB, name)
					if not os.path.exists(name):
						lib.git.clone(package, cwd = LIB)

	else:

		url = urllib.parse.urlparse(package)

		p = list(url)

		if url.scheme == '' : p[0] = 'http'

		if url.netloc == '':
			found = False
			for domain, vendor in VENDORS.items():
				p[1] = domain
				if lib.http.access(urllib.parse.urlunparse(p)):
					found = True
					break

			if not found:
				print('unable to find repo')
				return

		
		user, _ = urllib.parse.splituser(p[1])
		if user is None:
			vendor = VENDORS[p[1]]
			user = lib.config.prompt_user(p[1], vendor.__name__)
			p[1] = user + '@' + p[1]

		url = urllib.parse.urlunparse(p)

		lib.git.clone(url, cwd = LIB)

		if save in SAVE:
			which = SAVE[save]
			parts = os.path.split(p.path)
			name, _ = os.path.splitext(parts)
			with lib.cpm.package('w') as p:
				p[which][name] = url


def init():
	if not lib.cpm.configOK():
		with lib.cpm.package('w') as p:
			p['name'] = ''
			p['dep'] = {}
			p['dev'] = {}
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

	lib.cpm.libENSURE()