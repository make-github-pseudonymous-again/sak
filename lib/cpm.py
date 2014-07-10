

import lib.json, os.path

FILENAME_PACKAGE_CONFIGURATION = 'package.json'

LIB = 'lib'

class package(lib.json.proxy):

	def __init__(self, mode = 'r'):
		super().__init__(FILENAME_PACKAGE_CONFIGURATION, mode)



def configOK():
	return os.path.exists(FILENAME_PACKAGE_CONFIGURATION)

def libENSURE():
	if not os.path.exists(LIB):
		os.mkdir(LIB)

	elif not os.path.isdir(LIB):
		print('error -> lib exists and is not a directory')