import os, lib

file = os.path.expanduser('~/.sake')


def user(user):
	with lib.json.proxy(lib.config.file) as config : return config['u'].get(user, None)

def module(module):
	with lib.json.proxy(lib.config.file) as config :
		user = config['m'].get(module, None)
		passwd = config['u'].get(user, None)
		return user, passwd