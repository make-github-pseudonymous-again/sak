"""
	Main package containg all modules accessible through the $ command.
"""
import sys
import os
import lib

lib.pacman.__init__(sys.modules[__name__],
                    os.path.dirname(os.path.abspath(__file__)))
