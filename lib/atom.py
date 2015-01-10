import os.path


def project ( directory ) :

	path = os.path.abspath( directory )
	name = os.path.basename( path )

	return path, name
