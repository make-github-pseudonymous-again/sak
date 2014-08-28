from __future__ import absolute_import, division, print_function, unicode_literals

import os, sys, lib.file, lib.check

def concat(src, out):

	with open(out, 'w') as f:

		def callback(g):
			lib.file.read(g, f.write)
			f.write(os.linesep)

		lib.file.walk(src, callback)


def append(out, txt):

	with open(out, 'a') as f:
		f.write(txt)
		f.write(os.linesep)


TAB = "tab"
SPACE = "space"

INDENT_MODES = [TAB, SPACE]

INDENT_DEFAULT_WIDTH = {
	TAB : 1,
	SPACE : 4
}

INDENT_CHAR = {
	TAB : '\t',
	SPACE : ' '
}

def indent(src = sys.stdin, mode = TAB, width = None):

	lib.check.OptionNotInListException("mode", mode, INDENT_MODES)

	c = INDENT_CHAR[mode]

	if width is None : width = INDENT_DEFAULT_WIDTH[mode]

	lineprepend(src, c, width)


def lineprepend(src = sys.stdin, string = "", width = 1):

	width = int(width)
	sequence = string * width

	if src != sys.stdin :
		src = open(src, 'r')

	for line in src:
		print(sequence + line, end = '')

	if src != sys.stdin :
		src.close()
	
