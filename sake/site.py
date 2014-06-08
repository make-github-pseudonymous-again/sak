import os, lib


def down(directory = '.', config_file = 'json/config.json', dry_run = False):
	local = {'root' : os.path.abspath(directory)}

	pre = lambda *x: None

	def callback(helper, config):
		helper.server_down(config, local)

	if not lib.site.FTPSite.check_local_root(local['root']) : return
	lib.site.FTPSite.wrap(local, config_file, dry_run, pre, callback)

def up(directory = '.', config_file = 'json/config.json', dry_run = False):
	local = {'root' : os.path.abspath(directory)}

	pre = lambda *x: None

	def callback(helper, config):
		helper.server_up(config, local)

	if not lib.site.FTPSite.check_local_root(local['root']) : return
	lib.site.FTPSite.wrap(local, config_file, dry_run, pre, callback)


def diff(directory = '.', config_file = 'json/config.json'):
	return push(directory, config_file, dry_run = True)


def push(directory = '.', config_file = 'json/config.json', dry_run = False):

	local = {
		'root' : os.path.abspath(directory),
		'hash' : {},
		'tree' : {}
	}

	def pre(helper, config):
		helper.local_fetch(local['root'], config, local['hash'], local['tree'])

	def callback(helper, config):

		server = {
			'root' : config['root'],
			'hash' : {},
			'tree' : {}
		}

		helper.server_fetch(config, server)
		helper.update(config, local, server)

	if not lib.site.FTPSite.check_local_root(local['root']) : return
	lib.site.FTPSite.wrap(local, config_file, dry_run, pre, callback)


def hash(directory = '.', config_file = 'json/config.json'):
	local = {'root' : os.path.abspath(directory)}
	dry_run = False
	pre = lambda *args, **kwargs : None

	def callback(helper, config):

		server = {
			'hash' : {},
			'tree' : {}
		}

		helper.server_hash(config, server['hash'], server['tree'])
		helper.send_hash(config, server)

	lib.site.FTPSite.wrap(local, config_file, dry_run, pre, callback)



