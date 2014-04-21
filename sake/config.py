import getpass, json, os, lib

def gen():
	with open(lib.config.file, 'w') as f : lib.json.pretty({'u':{}, 'm':{}}, f)	

def cat():
	with open(lib.config.file, 'r') as f : lib.file.read(f, print)

def add(user, passwd):
	with lib.json.proxy(lib.config.file, 'w') as config : config['u'][user] = passwd

def rm(user):
	with lib.json.proxy(lib.config.file, 'w') as config : config['u'].pop(user)

def link(module, user):
	with lib.json.proxy(lib.config.file, 'w') as config : config['m'][module] = user

def unlink(module):
	with lib.json.proxy(lib.config.file, 'w') as config : config['m'].pop(module)

def user(user):
	print(lib.config.user(user))

def module(module):
	print(lib.config.module(module))
