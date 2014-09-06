from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
BIN = os.path.join(ROOT, "bin")
LIB = os.path.join(ROOT, "lib")
SAKE = os.path.join(ROOT, "sake")
DATA = os.path.join(ROOT, "data")

def data(*path):
	return os.path.join(DATA, *path)