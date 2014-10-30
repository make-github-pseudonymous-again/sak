# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import lib.file, base64


def hascii(path):
	with open(path, 'rb') as f : h = lib.file.hash(f).digest()
	return base64.b64encode(h).decode('ascii')
