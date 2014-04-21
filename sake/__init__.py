import sys, os, lib

lib.pacman.__init__(sys.modules[__name__], os.path.dirname(os.path.abspath(__file__)))