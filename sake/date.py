# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import subprocess

def timestamp():
	subprocess.call(['date', '+%s%N'])
