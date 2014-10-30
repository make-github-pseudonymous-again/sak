# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals


import subprocess


def do(action, *args):
	subprocess.call(['make', action] + args)

def install(*args):
	do('install', *args)

def clean(*args):
	do('clean', *args)

def all(*args):
	do('all', *args)
