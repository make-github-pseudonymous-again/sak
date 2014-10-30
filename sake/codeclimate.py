# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


import lib


def refresh(user, repo):

	lib.sys.call([
		'curl',
		'--data',
		'',
		'https://codeclimate.com/github/%s/%s/refresh' % (user, repo)
	])
