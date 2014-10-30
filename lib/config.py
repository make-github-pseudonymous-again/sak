# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os, lib, getpass

try :
	import urllib.parse as urllib
except :
	import urllib

fname = os.path.expanduser('~/.sake')

def new():
	return {'u':{}, 'm':{}}

def user(user):

	with lib.json.proxy(lib.config.fname, default = new()) as config :
		passwd = config['u'].get(user, None)

	return passwd

def module(module):

	with lib.json.proxy(lib.config.fname, default = new()) as config :
		user = config['m'].get(module, None)
		passwd = config['u'].get(user, None)

	return user, passwd



def prompt_cred(host, module, user = None, passwd = None, scheme = "https", port = 80):

	user = prompt_user(host, module, user, passwd, scheme, port)
	passwd = prompt_passwd(host, module, user, passwd, scheme, port)

	return user, passwd

def prompt_user(host, module, user = None, passwd = None, scheme = "https", port = 80):

	url = '%s://%s:%d' % (scheme, host, port)

	if user is None : user, passwd = lib.config.module(module)
	if user is None : user = input('Username for \'%s\' : ' % url)

	return user


def prompt_passwd(host, module, user, passwd = None, scheme = "https", port = 80):

	url = '%s://%s@%s:%d' % (scheme, urllib.quote_plus(user), host, port)

	if passwd is None : passwd = lib.config.user(user)
	if passwd is None : passwd = getpass.getpass('Password for \'%s\' : ' % url)

	return passwd


