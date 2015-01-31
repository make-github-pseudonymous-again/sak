import os , lib , lib.sys , os.path

def mount ( directory = '.' , dest = '~/www' ) :

	directory = os.path.abspath( os.path.expanduser( directory ) )
	dest = os.path.abspath( os.path.expanduser( dest ) )

	lib.sys.call( [ 'rm' , dest ] )
	lib.sys.call( [ 'ln' , '-s' , directory , dest ] )


def toggle(which, directory = '.', config_file = 'json/config.json', dry_run = False):
	local = {'root' : os.path.abspath(directory)}
	pre = lambda *args, **kwargs : None

	def callback(helper, config):
		helper.rswitch.toggle(config, local, which)

	if not lib.site.FTPSite.check_local_root(local['root']) : return
	lib.site.FTPSite.wrap(local, config_file, dry_run, pre, callback)


def down(directory = '.', config_file = 'json/config.json', dry_run = False):
	toggle('down', directory, config_file, dry_run)

def up(directory = '.', config_file = 'json/config.json', dry_run = False):
	toggle('up', directory, config_file, dry_run)


def clear ( target , directory = '.' , config_file = 'json/config.json' , dry_run = False ) :

	local = {
		'root' : os.path.abspath( directory ) ,
		'hash' : {} ,
		'tree' : {}
	}

	if not lib.site.FTPSite.check_local_root( local['root'] ) :
		return

	def pre ( helper , config ) :
		pass

	def callback ( helper , config ) :
		helper.remote.recursivermd( target )

	lib.site.FTPSite.wrap( local , config_file , dry_run , pre , callback )


def push(directory = '.', config_file = 'json/config.json', dry_run = False):

	local = {
		'root' : os.path.abspath(directory),
		'hash' : {},
		'tree' : {}
	}

	def pre(helper, config):
		helper.lfetch.local(local['root'], config, local['hash'], local['tree'])

	def callback(helper, config):

		server = {
			'root' : config['root'],
			'hash' : {},
			'tree' : {}
		}

		helper.rfetch.remote(config, server)
		helper.rupdater.all(config, local, server)

	if not lib.site.FTPSite.check_local_root(local['root']) : return
	lib.site.FTPSite.wrap(local, config_file, dry_run, pre, callback)


def diff(directory = '.', config_file = 'json/config.json'):
	return push(directory, config_file, dry_run = True)



def hash(directory = '.', config_file = 'json/config.json'):
	local = {'root' : os.path.abspath(directory)}
	dry_run = False
	pre = lambda *args, **kwargs : None

	def callback(helper, config):

		server = {
			'hash' : {},
			'tree' : {}
		}

		helper.rhasher.hash(config, server['hash'], server['tree'])
		helper.rhasher.send(config, server)

	lib.site.FTPSite.wrap(local, config_file, dry_run, pre, callback)



