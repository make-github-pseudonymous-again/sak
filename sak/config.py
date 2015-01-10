import lib.config, lib.json, lib.file

def gen():
	with open(lib.config.fname, 'w') as f : lib.json.pretty(lib.config.new(), f)

def cat():
	with open(lib.config.fname, 'r') as f : lib.file.read(f, print)

def add(user, passwd):
	with lib.config.proxy( 'w' ) as config : config['u'][user] = passwd

def rm(user):
	with lib.config.proxy( 'w' ) as config : config['u'].pop(user)

def link(module, user):
	with lib.config.proxy( 'w' ) as config : config['m'][module] = user

def unlink(module):
	with lib.config.proxy( 'w' ) as config : config['m'].pop(module)

def user(user):
	print(lib.config.user(user))

def module(module):
	print(lib.config.module(module))
